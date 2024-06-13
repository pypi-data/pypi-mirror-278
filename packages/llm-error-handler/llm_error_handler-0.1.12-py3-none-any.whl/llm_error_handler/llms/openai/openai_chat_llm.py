import json
import logging
import numpy as np
import requests
import queue
import sys
import threading
from typing import Any, Dict, Generator, List, Optional, Tuple, Union
import traceback
from openai import OpenAI
from .openai_chat_history import OpenAIChatHistory
from ..llm_utils.adjust_llm_json import adjust_llm_json
from ..llm_utils.mix_in import InitializeLLMMixIn, InitializeChatMethodMixIn, ChatUtilsMixIn, JsonModeMixIn

class OpenAIChatLLM(InitializeLLMMixIn, InitializeChatMethodMixIn, ChatUtilsMixIn, JsonModeMixIn):
    def __init__(
        self, 
        model: str = "gpt-4o",
        system_message: str = "",
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: str = "none",
        tool_object: Optional[object] = None,
        temperature: float = 0.8,
        max_tokens: int = 2048
    ):
        self.llm_type = "openai"
        self.llm = OpenAI()
        self.model = model
        self.client = self.llm
        self.system_message = system_message
        self.tool_object = tool_object
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tool_choice = tool_choice
        self.tools = tools
        self.stream = False
        
        self._initialize_configs()

        self.history = OpenAIChatHistory(
            messages=messages, 
            tools=self.tools, 
            max_total_tokens=self.max_total_tokens, 
            max_response_tokens=self.max_tokens, 
            model=self.model
        )
        self._initialize_messages(self.system_message, messages)

        logging.debug(f"""
---OpenAIChatLLM is initialized---
model: {self.model}
temperature: {self.temperature}
max_tokens: {self.max_tokens}
tool_choice: {self.tool_choice}
tools: {self.tools}
initial_messages: {self.init_messages}
----------------------------------""")
        
        
    def chat(
        self, 
        user_input: str, 
        file_path_list: Optional[List[str]] = None, 
        image_detail: str = "high", 
        model: Optional[str] = None, 
        system_message: Optional[str] = None, 
        messages: Optional[List[dict]] = None, 
        tools: Optional[List[dict]] = None, 
        tool_choice: Optional[str] = None, 
        tool_object: Optional[object] = None, 
        temperature: Optional[float] = None, 
        max_tokens: Optional[int] = None,
        mode: Optional[str] = None
    ) -> Union[str, dict]:
        
        try:
            self.history.add_message(role="user", text=user_input, image_list=file_path_list, detail=image_detail)
            self.stream = False

            model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use = self._initialize_chat_parameters(model, system_message, messages, tools, tool_choice, tool_object, temperature, max_tokens)
            chat_response = self._handle_response(model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use, mode)
            return chat_response
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            return "Network error, please try again later."
        except Exception as e:
            logging.error(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            raise RuntimeError(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            
        
    def stream_chat(
        self, 
        user_input: str, 
        file_path_list: Optional[List[str]] = None, 
        image_detail: str = "high", 
        model: Optional[str] = None, 
        system_message: Optional[str] = None, 
        messages: Optional[List[dict]] = None, 
        tools: Optional[List[dict]] = None, 
        tool_choice: Optional[str] = None, 
        tool_object: Optional[object] = None, 
        temperature: Optional[float] = None, 
        max_tokens: Optional[int] = None,
        mode: Optional[str] = None,
        json_keys: Optional[List[str]] = None
    ) -> Generator[str, None, None]:
        
        try:
            self.history.add_message(role="user", text=user_input, image_list=file_path_list, detail=image_detail)
            self.stream = True
            model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use = self._initialize_chat_parameters(model, system_message, messages, tools, tool_choice, tool_object, temperature, max_tokens)
            
            self.history.existing_messages_tokens + self.history.additional_message_tokens
            
            response_q = queue.Queue()
            thread = threading.Thread(target=self._stream_response_to_queue, args=(response_q, model_to_use, messages_to_use, temperature_to_use, max_tokens_to_use, tools_to_use, tool_choice_to_use))
            thread.start()
            
            content, function_name, function_arguments, function_call = "", "", "", False
            
            if mode == "json":
                json_response_q = queue.Queue()
                thread = threading.Thread(target=self._yield_json_response, args=(response_q, json_response_q, json_keys))
                thread.start()
                while True:
                    json_token = json_response_q.get()
                    sys.stdout.flush()
                    if json_token[0] == "final json result":
                        yield json_token
                        break
                    yield json_token
                    
            else:
                while True:
                    token = response_q.get()
                    if token is None:
                        break
                    
                    token_type, token_chunk = self._stream_response(token)
                    if token_type == "content":
                        content += token_chunk
                        sys.stdout.flush()
                        yield token_chunk
                    elif token_type == "function_name":
                        function_name += token_chunk
                        function_call = True
                    elif token_type == "function_arguments":
                        function_arguments += token_chunk
                        function_call = True
                        
            if content:
                self.history.add_message(role="assistant", text=content)

            if function_call:
                result: str = self._execute_tool_call(tool_object_to_use, function_name, function_arguments)
                self.history.add_message(role="function", text=f"function_result: {result}", function_name=function_name)
                messages_to_use.append({"role": "function", "content": [{"type": "text", "text": result}]})

                function_response_q = queue.Queue()
                function_thread = threading.Thread(target=self._stream_response_to_queue, args=(function_response_q, model_to_use, messages_to_use, temperature_to_use, max_tokens_to_use))
                function_thread.start()
                
                function_content = ""
                if mode == "json":
                    function_json_response_q = queue.Queue()
                    thread = threading.Thread(target=self._yield_json_response, args=(function_response_q, function_json_response_q, json_keys))
                    thread.start()
                    while True:
                        function_json_token = function_json_response_q.get()
                        sys.stdout.flush()
                        if function_json_token[0] == "final json result":
                            yield function_json_token
                            break
                        yield function_json_token
                else:
                    while True:
                        token = function_response_q.get()
                        if token is None:
                            break
                        function_token_type, function_token_chunk = self._stream_response(token)
                        if function_token_type == "content":
                            function_content += function_token_chunk
                            sys.stdout.flush()
                            yield function_token_chunk
                self.history.add_message(role="assistant", text=function_content)
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            yield "Network error, please try again later."
        except Exception as e:
            logging.error(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            raise RuntimeError(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            
    def run(
        self,
        model: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        tool_object: Optional[object] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        mode: Optional[str] = None
    ) -> str:
        try:
            self.stream = False
            model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use = self._initialize_run_parameters(model, messages, tools, tool_choice, tool_object, temperature, max_tokens)
            chat_response = self._handle_response(model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use, mode)
            return chat_response
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            return "Network error, please try again later."
        except Exception as e:
            logging.error(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            raise RuntimeError(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
        
    def stream_run(
        self,
        model: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        tool_object: Optional[object] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        mode: Optional[str] = None,
        json_keys: Optional[List[str]] = None
    ) -> Generator[str, None, None]:
        try:
            self.stream = True
            model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use = self._initialize_run_parameters(model, messages, tools, tool_choice, tool_object, temperature, max_tokens)
            
            response_q = queue.Queue()
            thread = threading.Thread(target=self._stream_response_to_queue, args=(response_q, model_to_use, messages_to_use, temperature_to_use, max_tokens_to_use, tools_to_use, tool_choice_to_use))
            thread.start()
            
            content, function_name, function_arguments, function_call = "", "", "", False
            
            if mode == "json":
                json_response_q = queue.Queue()
                thread = threading.Thread(target=self._yield_json_response, args=(response_q, json_response_q, json_keys))
                thread.start()
                while True:
                    json_token = json_response_q.get()
                    sys.stdout.flush()
                    if json_token[0] == "final json result":
                        yield json_token
                        break
                    yield json_token
                    
            else:
                while True:
                    token = response_q.get()
                    if token is None:
                        break
                    
                    token_type, token_chunk = self._stream_response(token)
                    if token_type == "content":
                        content += token_chunk
                        sys.stdout.flush()
                        yield token_chunk
                    elif token_type == "function_name":
                        function_name += token_chunk
                        function_call = True
                    elif token_type == "function_arguments":
                        function_arguments += token_chunk
                        function_call = True

            if function_call:
                result: str = self._execute_tool_call(tool_object_to_use, function_name, function_arguments)
                self.history.add_message(role="function", text=f"function_result: {result}", function_name=function_name)
                messages_to_use.append({"role": "function", "content": [{"type": "text", "text": result}]})

                function_response_q = queue.Queue()
                function_thread = threading.Thread(target=self._stream_response_to_queue, args=(function_response_q, model_to_use, messages_to_use, temperature_to_use, max_tokens_to_use))
                function_thread.start()
                
                function_content = ""
                
                if mode == "json":
                    function_json_response_q = queue.Queue()
                    thread = threading.Thread(target=self._yield_json_response, args=(function_response_q, function_json_response_q, json_keys))
                    thread.start()
                    while True:
                        function_json_token = function_json_response_q.get()
                        sys.stdout.flush()
                        if function_json_token[0] == "final json result":
                            yield function_json_token
                            break
                        yield function_json_token
                else:
                    while True:
                        token = function_response_q.get()
                        if token is None:
                            break
                        function_token_type, function_token_chunk = self._stream_response(token)
                        if function_token_type == "content":
                            function_content += function_token_chunk
                            sys.stdout.flush()
                            yield function_token_chunk
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            yield "Network error, please try again later."
        except Exception as e:
            logging.error(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
            raise RuntimeError(f"Exception occurred during stream chat: {str(e)}\n{traceback.format_exc()}")
    
    """
    token数計算実装未
    """
    def make_json(self, user_input, system_message = "You are a helpful assistant designed to output JSON."):
        #self.modelがgpt-4-1106-preview,gpt-3.5-turbo-1106以外の時はエラーを出す。
        if self.model != "gpt-4-1106-preview" and self.model != "gpt-3.5-turbo-1106":
            raise ValueError(f"Invalid model for json_mode: {self.model}, only gpt-4-1106-preview and gpt-3.5-turbo-1106 are supported.")
        response_format = { "type": "json_object" }
        messages=[
            {"role": "system", "content": [{"type":"text", "text":system_message}]},
            {"role": "user", "content": [{"type":"text", "text":user_input}]}
        ]
        response = self.client.chat.completions.create(messages = messages, model = self.model, temperature = self.temperature, max_tokens = self.max_tokens, response_format = response_format)
        response_json_str = response.choices[0].message.content
        response_json = adjust_llm_json(response_json_str)
        return response_json
    
    def get_datas(self, user_input, tool_name, system_message = ""):
        # tools もしくは tool_choiceがない場合はエラーを出す。
        if self.tools == None or self.tool_choice == "none":
            raise ValueError(f"Invalid tools or tool_choice for get_datas: {self.tools}, {self.tool_choice}")
        #self.modelがgpt-4-1106-preview,gpt-3.5-turbo-1106以外の時はエラーを出す。
        if self.model != "gpt-4-1106-preview" and self.model != "gpt-3.5-turbo-1106":
            raise ValueError(f"Invalid model for get_datas: {self.model}, only gpt-4-1106-preview and gpt-3.5-turbo-1106 are supported.")
        tool_choice = { "type" : "function", "function" : {"name": f"{tool_name}"}}
        messages = [
            {"role": "system", "content": [{"type":"text", "text":system_message}]},
            {"role": "user", "content": [{"type":"text", "text":user_input}]}
        ]
        response = self.client.chat.completions.create(messages = messages, model = self.model, temperature = self.temperature, max_tokens = self.max_tokens, tool_choice = tool_choice, tools = self.tools)
        response_datas = response.choices[0].message.tool_calls[0].function.arguments
        response_datas = json.loads(response_datas)

        return response_datas
    

    def create(self, messages, **kwargs):
        try:
            response = self.llm.chat.completions.create(messages = messages, **kwargs)
        except:
            response = None
        return response
    
    def get_embedding(self, text):
        response = self.llm.embeddings.create(input=text, model='text-embedding-3-large')
        return np.array(response.data[0].embedding)
        
    def _get_tool_names(self):
        return [f['function']['name'] for f in self.tools]

    def _create_chat_completion(
        self,
        model: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Any:
        try:
            if tool_choice != "none" and tools:
                return self.client.chat.completions.create(
                    messages=messages, 
                    model=model, 
                    temperature=temperature,
                    max_tokens=max_tokens, 
                    stream=self.stream, 
                    tool_choice=tool_choice, 
                    tools=tools
                )
            else:
                return self.client.chat.completions.create(
                    messages=messages, 
                    model=model, 
                    temperature=temperature,
                    max_tokens=max_tokens, 
                    stream=self.stream
                )
        except Exception as e:
            logging.error(f"Exception occurred during chat completion creation: {str(e)}")
            raise RuntimeError(f"Exception occurred during chat completion creation: {str(e)}")

    def _get_delta(self, token):
        delta = token.choices[0].delta
        return delta
    
    def _get_message(self, response):
        message = response.choices[0].message
        return message
    
    def _get_content(self, response):
        if response.content:
            content = response.content
            return content
        return ""
    
    def _get_function_name(self, response):
        if response.tool_calls:
            if response.tool_calls[0].function.name:
                function_name = response.tool_calls[0].function.name
                return function_name
        return ""
    
    def _get_function_arguments(self, response):
        if response.tool_calls:
            if response.tool_calls[0].function.arguments:
                function_arguments = response.tool_calls[0].function.arguments
                return function_arguments
        return ""

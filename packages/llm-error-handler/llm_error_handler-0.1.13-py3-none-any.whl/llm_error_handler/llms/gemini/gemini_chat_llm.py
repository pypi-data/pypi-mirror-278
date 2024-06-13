import json
import logging
import numpy as np
import os
import re
import sys
import threading
from typing import Any, Dict, Generator, List, Optional, Tuple, Union
import traceback
import queue
import requests
import google.generativeai as genai
import google.ai.generativelanguage as glm
from .gemini_chat_history import GeminiChatHistory
from .change_utils import change_messages_for_gemini
from ..llm_utils.adjust_llm_json import adjust_llm_json
from ..llm_utils.mix_in import InitializeLLMMixIn, InitializeChatMethodMixIn, ChatUtilsMixIn, JsonModeMixIn

class GeminiChatLLM(InitializeLLMMixIn, InitializeChatMethodMixIn, ChatUtilsMixIn, JsonModeMixIn):
    def __init__(
        self, 
        model: str = "gemini-1.5-flash-latest", 
        system_message: str = "", 
        messages: Optional[List[dict]] = None, 
        tools: Optional[List[dict]] = None, 
        tool_choice: str = "none", 
        tool_object: Optional[object] = None, 
        temperature: float = 0.8, 
        max_tokens: int = 2048
    ):
        self.llm_type = "gemini"
        self.llm = self._configure_genai()
        self.model = model
        self.client = self.llm
        self.system_message = system_message
        self.tool_object = tool_object
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tool_choice = tool_choice
        self.tools = tools
        self.stream = False
        self.converted_tools = self._convert_json_to_glm_tool(tools)
        
        self._initialize_configs()

        self.history = GeminiChatHistory(
            messages=messages, 
            tools=self.tools, 
            max_total_tokens=self.max_total_tokens, 
            max_response_tokens=self.max_tokens, 
            model=self.model
        )
        self._initialize_messages(self.system_message, messages)

        self.config = self.client.GenerationConfig(
            temperature=self.temperature, 
            max_output_tokens=self.max_tokens
        )

        logging.debug(f"""
---GeminiChatLLM is initialized---
model: {self.model}
temperature: {self.temperature}
max_tokens: {self.max_tokens}
tool_choice: {self.tool_choice}
tools: {self.converted_tools}
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
    ) -> Union[str, dict]:
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
                
    def make_json(self, user_input, system_message = "You are a helpful assistant designed to output JSON."):
        messages=[
            {"role": "user", "parts": [system_message]},
            {"role": "user", "content": [user_input]}
        ]
        llm = self.client.GenerativeModel(model_name = self.model)
        response = llm.generate_content(messages = messages, generation_config = self.config)
        response_json = response.text
        return response_json
            
    def get_datas(self, user_input, tool_name, system_message = ""):
        # tools もしくは tool_choiceがない場合はエラーを出す。
        if self.converted_tools == [] or self.tool_choice == "none":
            raise ValueError(f"Invalid tools or tool_choice for get_datas: {self.converted_tools}, {self.tool_choice}")
        tool_choice = { "type" : "function", "function" : {"name": f"{tool_name}"}}
        messages = [
            {"role": "user", "content": [{"type":"text", "text":system_message}]},
            {"role": "user", "content": [{"type":"text", "text":user_input}]}
        ]
        llm = self.client.GenerativeModel(model_name = self.model)
        response = llm.generate_content(messages = messages, generation_config = self.config)
        response_datas = response.candidates[0].content.parts[0].function_call.args
        response_datas_json = {k:v for k, v in response_datas.items() if v is not None}

        return response_datas_json

    def create(self, messages, **kwargs):
        try:
            model_name = kwargs.get('model', self.model)
            model = self.llm.GenerativeModel(model_name)
            changed_messages = change_messages_for_gemini(messages)
            response = model.generate_content(changed_messages)
        except:
            response = None
        return response
    
    def get_embedding(self, text):
        try:
            response = self.llm.embed_content(model="models/embedding-001", content=text)
            return np.array(response['embedding'])
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def _configure_genai(self) -> genai:
        GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)
        return genai


    def _convert_json_to_glm_tool(self, tools_json):
        function_declarations = []
        if tools_json:
            for tool in tools_json:
                func = tool['function']
                properties = {}
                for param_name, param_info in func['parameters']['properties'].items():
                    # OpenAPIの型をglm.Typeに変換
                    if param_info['type'] == 'array':
                        item_type = getattr(glm.Type, param_info['items']['type'].upper(), glm.Type.STRING)
                        glm_type = glm.Type.ARRAY
                        properties[param_name] = glm.Schema(type=glm_type, items=glm.Schema(type=item_type), description=param_info.get('description', ''))
                    else:
                        glm_type = getattr(glm.Type, param_info['type'].upper(), glm.Type.STRING)
                        properties[param_name] = glm.Schema(type=glm_type, description=param_info.get('description', ''))
                parameters = glm.Schema(type=glm.Type.OBJECT, properties=properties, required=func['parameters'].get('required', []))
                function_declaration = glm.FunctionDeclaration(name=func['name'], description=func.get('description', ''), parameters=parameters)
                function_declarations.append(function_declaration)

        return glm.Tool(function_declarations=function_declarations)
        
    def _get_tool_names(self):
        return [f.name for f in self.converted_tools.function_declarations]
        
    def _check_non_str_in_parts(self):
        for message in self.history.messages:
            # partsキーが存在するか確認
            if 'parts' in message:
                # partsリスト内の各要素がstr型でないかチェック
                if any(not isinstance(part, str) for part in message['parts']):
                    return True  # str型以外が含まれている
        return False  # すべてのpartsがstr型のみから成る
            
    def _create_chat_completion(
        self,
        model: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        config: Optional[dict] = None,
        **kwargs
    ) -> Any:
        try:
            if tool_choice != "none" and tools:
                llm = self.client.GenerativeModel(model_name = model, tools = tools)
            else:
                llm = self.client.GenerativeModel(model_name = model)

            return llm.generate_content(contents = messages, generation_config = config, stream = self.stream)
        except Exception as e:
            logging.error(f"Exception occurred during stream chat: {str(e)}")
            raise RuntimeError(f"Exception occurred during stream chat: {str(e)}")
    
    def _get_delta(self, token):
        delta = token.candidates[0].content
        return delta
    
    def _get_message(self, response):
        message = response.candidates[0].content
        return message
    
    def _get_content(self, response):
        if response.parts:
            if response.parts[0].text:
                content = response.parts[0].text
                return content
        return ""
    
    def _get_function_name(self, response):
        if response.parts:
            if response.parts[0].function_call.name:
                function_name = response.parts[0].function_call.name
                return function_name
        return ""
    
    def _get_function_arguments(self, response):
        if response.parts:
            if response.parts[0].function_call.args:
                function_arguments = response.parts[0].function_call.args
                return function_arguments
        return ""


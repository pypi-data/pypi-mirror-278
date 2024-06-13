import re
import sys
import json
import logging
import os
from typing import List, Optional, Tuple, Generator, Dict, Any
from ..llm_utils.adjust_llm_json import adjust_llm_json

class InitializeLLMMixIn:
    def _load_llm_configs(self, config_path: str) -> dict:
        try:
            with open(config_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError as e:
            logging.error(f"Configuration file {config_path} not found: {e}")
            raise FileNotFoundError(f"Configuration file {config_path} not found: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from configuration file {config_path}: {e}")
            raise json.JSONDecodeError(f"Error decoding JSON from configuration file {config_path}: {e}")

    def _validate_model(self, llm_configs: dict, model: str):
        if model not in llm_configs[self.llm_type]:
            logging.error(f"Invalid model: {model}")
            raise ValueError(f"Invalid model: {model}")
        
    def _initialize_configs(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        llm_configs = self._load_llm_configs(os.path.join(current_dir, "../configs/llm_configs/llm_models.json"))
        self._validate_model(llm_configs, self.model)
        self.max_total_tokens = llm_configs[self.llm_type][self.model]["max_tokens"]
    
    def _initialize_messages(self, system_message: str, messages: Optional[List[dict]]):
        if system_message:
            self.history.messages.insert(0, {"role": "system", "content": [{"type": "text", "text": system_message}]})
        
        if messages:
            self.history.messages += messages
        else:
            self.history.messages += []

        self.init_messages = self.history.messages.copy()
        
class InitializeChatMethodMixIn:
    def _handle_response(
        self,
        model: str,
        messages: List[dict],
        tools: Optional[List[dict]],
        tool_choice: str,
        tool_object: Optional[object],
        temperature: float,
        max_tokens: int,
        mode: Optional[str]
    ):
            response = self._create_chat_completion(
                model = model,
                messages = messages,
                tools = tools,
                tool_choice = tool_choice,
                temperature = temperature,
                max_tokens = max_tokens
            )
            message = self._get_message(response)
            content = self._get_content(message)
            function_name = self._get_function_name(message)
            function_arguments = self._get_function_arguments(message)

            if content:
                chat_response = content
                self.history.add_message(role = "assistant", text = chat_response)
            elif function_name:
                result = self._execute_tool_call(tool_object, function_name, function_arguments)
                self.history.add_message(role = "function", text = f"function_result: {result}", function_name = function_name)
                function_response = self._create_chat_completion(
                    messages = self.history.messages, 
                    model = model, 
                    temperature = temperature, 
                    max_tokens = max_tokens, 
                    stream = self.stream
                )
                function_message = self._get_message(function_response)
                chat_response = self._get_content(function_message)
                self.history.add_message(role = "assistant", text = chat_response)
                
            if mode == "json":
                chat_response = adjust_llm_json(chat_response)
                if not chat_response:
                    logging.error("mode is json but json is not found.")
            
            return chat_response
        
    def _stream_response_to_queue(self, q, model, messages, temperature, max_tokens, tools = None, tool_choice = "none"):
        response = self._create_chat_completion(
            model = model,
            messages = messages,
            tools = tools,
            tool_choice = tool_choice,
            temperature = temperature,
            max_tokens = max_tokens,
        )
        for token in response:
            q.put(token)
        q.put(None)  
        
    def _initialize_chat_parameters(
        self,
        model: Optional[str] = None,
        system_message: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        tool_object: Optional[object] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        messages_to_use = messages if messages else self.history.messages.copy()
        if system_message:
            if messages_to_use[0]["role"] == "system":
                messages_to_use.pop(0)
            messages_to_use.insert(0, {"role": "system", "content": [{"type": "text", "text": system_message}]})
        model_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use = self._initialize_common_configs(model, tools, tool_choice, tool_object, temperature, max_tokens)
        return model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use
    
    def _initialize_run_parameters(
        self,
        model: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        tool_object: Optional[object] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        if messages:
            messages_to_use = messages
        else:
            if self.init_messages:
                messages_to_use = self.init_messages.copy()
            else:
                messages_to_use = []
        model_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use = self._initialize_common_configs(model, tools, tool_choice, tool_object, temperature, max_tokens)
        return model_to_use, messages_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use
    
    def _initialize_common_configs(
        self,
        model: Optional[str] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        tool_object: Optional[object] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        model_to_use = model if model else self.model
        tool_choice_to_use = tool_choice if tool_choice else self.tool_choice
        tool_object_to_use = tool_object if tool_object else self.tool_object
        temperature_to_use = temperature if temperature else self.temperature
        max_tokens_to_use = max_tokens if max_tokens else self.max_tokens
        if tools:
            tools_to_use = tools
        else:
            if self.tools:
                tools_to_use = self.tools.copy()
            else:
                tools_to_use = None
        return model_to_use, tools_to_use, tool_choice_to_use, tool_object_to_use, temperature_to_use, max_tokens_to_use

class ChatUtilsMixIn:
    def clear_chat(self):
        self.history.messages = self.init_messages
        
    def _stream_response(self, token) -> Generator[Tuple[str, str], None, None]:
        try:
            content, function_name, function_arguments = self._get_content_and_function_call(token)
            if content:
                return ("content", content)
            if function_name != "":
                return ("function_name", function_name)
            if function_arguments != "":
                return ("function_arguments", function_arguments)
            return ("content", content)
        except Exception as e:
            logging.error(f"Exception occurred during stream chat: {str(e)}")
            raise RuntimeError(f"Exception occurred during stream chat: {str(e)}")
        
    def _get_content_and_function_call(self, token):
        delta = self._get_delta(token)
        content = self._get_content(delta)
        function_name = self._get_function_name(delta)
        function_arguments = self._get_function_arguments(delta)
        return content, function_name, function_arguments
    
    def _execute_tool_call(self, tool_object: object, name: str, arguments: str) -> str:
        try:
            results: Optional[str] = None
            tool_names: List[str] = self._get_tool_names()
            arguments: Dict[str, Any] = {k: v for k, v in arguments.items() if v is not None}

            if tool_object:
                if name in tool_names:
                    tool = getattr(tool_object, name)
                    if callable(tool):
                        results = tool(**arguments)
                    else:
                        results = f"Error: {name} is not a function"
                else:
                    results = f"Error: function {name} does not exist"
            else:
                results = f"Error: tool_object is None or function {name} is not in tool_names"

            logging.info(f"Executed tool call: {name} with arguments: {arguments}, results: {results}")
            return results
        except Exception as e:
            logging.error(f"Exception occurred during tool call: {str(e)}")
            return f"Exception occurred during tool call: {str(e)}"

class JsonModeMixIn:
    def _yield_json_response(self, response_q, json_response_q, json_keys):
        all_buffer: str = ""
        json_buffer: str = ""
        new_value_token: str = ""
        in_json: bool = False
        current_key: Optional[str] = None
        value_buffer: str = ""
        value_type: Optional[str] = None
        top_of_detected_key: bool = True
        detected_key_and_values: Optional[dict] = None
        previous_detected_key: Optional[str] = None
        key_patterns = self._create_key_patterns(json_keys)
            
        while True:
            token = response_q.get()
            if token is None:
                break
            token_type, token_chunk = self._stream_response(token)
            in_json = self._detect_json_start(token_chunk, in_json)
            new_value_token = token_chunk
            if not new_value_token:
                new_value_token = ""
            all_buffer += new_value_token
            
            if in_json:
                if detected_key_and_values:
                    previous_detected_key = detected_key_and_values[0]["key"]
                detected_key_and_values = []
                if not json_buffer:
                    new_value_token = self._delete_before_json(new_value_token)
                json_buffer += new_value_token
                detected_key_and_values = self._detect_key(json_buffer, key_patterns)
                if detected_key_and_values:
                    if detected_key_and_values[0]["key"] != previous_detected_key:
                        top_of_detected_key = True
                if len(detected_key_and_values) > 1:
                    for i, key_and_value in enumerate(detected_key_and_values):
                        if key_and_value:
                            current_key = key_and_value["key"]
                            if i == len(detected_key_and_values) - 1:
                                value_buffer = key_and_value["value"]
                                value_type = self._determine_value_type(value_buffer)
                                value_end_bool, value_end = self._handle_value_end(value_type, value_buffer)
                                if value_end_bool:
                                    key_patterns.pop(current_key)
                                    if value_type == "string":
                                        match = re.search(r'",\s*', new_value_token)
                                        new_value_token = new_value_token[:match.start()]
                                    else:
                                        value_end_pos = new_value_token.rfind(',')
                                        new_value_token = new_value_token[:value_end_pos]
                                if top_of_detected_key:
                                    if value_buffer:
                                        top_of_detected_key = False
                                    new_value_token = value_end
                                    if value_type == "string":
                                        new_value_token = new_value_token.strip('"')
                                json_response_q.put((current_key, new_value_token))
                            else:
                                key_patterns.pop(current_key)
                                value_buffer = key_and_value["value"]
                                value_token = value_buffer
                                json_response_q.put((current_key, value_token))
                else:
                    if detected_key_and_values:
                        current_key = detected_key_and_values[0]["key"]
                        value_buffer = detected_key_and_values[0]["value"]
                        value_type = self._determine_value_type(value_buffer)
                        value_end_bool, value_end = self._handle_value_end(value_type, value_buffer)
                        if value_end_bool:
                            key_patterns.pop(current_key)
                            if value_type == "string":
                                match = re.search(r'",\s*', new_value_token)
                                new_value_token = new_value_token[:match.start()]
                            else:
                                value_end_pos = new_value_token.rfind(',')
                                new_value_token = new_value_token[:value_end_pos]
                        if top_of_detected_key:
                            if value_buffer:
                                top_of_detected_key = False
                            new_value_token = value_end
                            if value_type == "string":
                                new_value_token = new_value_token.strip('"')
                        json_response_q.put((current_key, new_value_token))
            
        json_end_index = json_buffer.rfind('}')
        try:
            final_json_result = json.loads(json_buffer[:json_end_index + 1])
            json_response_q.put(("final json result", final_json_result))
        except Exception as e:
            logging.error(f"Error occurred during json mode stream chat and json cannot be decoded.\n all_buffer: {all_buffer}\njson_buffer: {json_buffer}\nError: {e}")
            raise RuntimeError(f"Error occurred during json mode stream chat and json cannot be decoded.\n all_buffer: {all_buffer}\njson_buffer: {json_buffer}\nError: {e}")
    
    def _create_key_patterns(self, keys: List[str]) -> dict:
        return {key: re.compile(rf'"{key}"\s*:\s*') for key in keys}

    def _detect_json_start(self, token: str, in_json: bool) -> bool:
        if token:
            return in_json or '{' in token
        return in_json
    
    def _delete_before_json(self, buffer: str) -> str:
        if buffer and buffer.find('{') != -1:
            buffer = buffer[buffer.find('{') + 0:]
        return buffer

    def _detect_key(self, json_buffer: str, key_patterns: dict) -> List[dict]:
        detected_key_and_values: List[dict] = []
        value_buffer: str = ""
        key_pattern_pos_list: List[dict] = []
        for key, pattern in key_patterns.items():
            match = pattern.search(json_buffer)
            if match:
                start_key_pattern_char_pos = match.start()
                end_key_pattern_char_pos = match.end()
                key_pattern_pos_list.append({"key": key, "start_key_pattern_char_pos": start_key_pattern_char_pos, "end_key_pattern_char_pos": end_key_pattern_char_pos})
            
        if key_pattern_pos_list:
            start_value_char_pos = key_pattern_pos_list[0]["end_key_pattern_char_pos"]
            first_key = key_pattern_pos_list[0]["key"]
            key_pattern_pos_list.pop(0)
            if len(key_pattern_pos_list) == 0:
                value_buffer = json_buffer[start_value_char_pos:]
                detected_key_and_values = self._extract_key_and_values(detected_key_and_values, first_key, value_buffer)
            elif len(key_pattern_pos_list) > 0:
                value_buffer = json_buffer[start_value_char_pos:]
                detected_key_and_values = self._extract_key_and_values(detected_key_and_values, first_key, value_buffer)
                for i, key_pattern_pos in enumerate(key_pattern_pos_list):
                    start_value_char_pos = key_pattern_pos["end_key_pattern_char_pos"]
                    if i == len(key_pattern_pos_list) - 1:
                        value_buffer = json_buffer[start_value_char_pos:]
                        detected_key_and_values = self._extract_key_and_values(detected_key_and_values, key_pattern_pos["key"], value_buffer)
                    else:
                        end_value_char_pos = key_pattern_pos["start_key_pattern_char_pos"]
                        value_buffer = json_buffer[start_value_char_pos:end_value_char_pos]
                        detected_key_and_values = self._extract_key_and_values(detected_key_and_values, key_pattern_pos["key"], value_buffer)
                    
        return detected_key_and_values

    def _determine_value_type(self, value_buffer: str) -> Optional[str]:
        stripped_value_buffer = value_buffer.strip()
        if stripped_value_buffer.startswith('"'):
            return 'string'
        elif re.match(r'^-?\d+(\.\d+)?([eE][+-]?\d+)?\s*,?', stripped_value_buffer):
            return 'number'
        elif stripped_value_buffer.startswith('{'):
            return 'object'
        elif stripped_value_buffer.startswith('['):
            return 'array'
        elif stripped_value_buffer in ('true', 'false'):
            return 'boolean'
        elif stripped_value_buffer == 'null':
            return 'null'
        return None

    def _handle_value_end(self, value_type: str, value_buffer: str) -> Tuple[bool, str]:
        
        if value_type == 'string':
            # 文字列がエスケープされていないダブルクォートで終了するかを判定
            in_string = False
            out_string = False
            value_end_pos = -1
            for i, char in enumerate(value_buffer):
                if char == '"' and (i == 0 or value_buffer[i - 1] != '\\') and not in_string:
                    in_string = True
                elif char == '"' and (i == 0 or value_buffer[i - 1] != '\\') and in_string:
                    out_string = True
                    value_end_pos = i + 1
                    break
            if out_string:
                if value_end_pos != -1:
                    value = value_buffer[:value_end_pos]
                    return True, value
                else:
                    value = value_buffer
                    return True, value
        
        elif value_type == 'number':
            # 数値の終了条件を修正
            end_comma_pos = value_buffer.find(',')
            if end_comma_pos != -1:
                value_end_pos = end_comma_pos
                if value_end_pos != -1:
                    value = value_buffer[:value_end_pos + 1]
                    return True, value
                else:
                    value = value_buffer
                    return True, value
        
        elif value_type == 'object':
            # オブジェクトの終了条件を修正
            start_brace_count, end_brace_count = 0, 0
            start_brace_count += value_buffer.count('{')
            end_brace_count += value_buffer.count('}')
            brace_count = start_brace_count - end_brace_count
            if brace_count == 0:
                value_end_pos = value_buffer.rfind('}')
                if value_end_pos != -1:
                    value = value_buffer[:value_end_pos + 1]
                    return True, value
                else:
                    value = value_buffer
                    return True, value

        elif value_type == 'array':
            # 配列の終了条件を修正
            start_bracket_count, end_bracket_count = 0, 0
            start_bracket_count += value_buffer.count('[')
            end_bracket_count += value_buffer.count(']')
            bracked_count = start_bracket_count - end_bracket_count
            if bracked_count == 0:
                value_end_pos = value_buffer.rfind(']')
                if value_end_pos != -1:
                    value = value_buffer[:value_end_pos + 1]
                    return True, value
                else:
                    value = value_buffer
                    return True, value
        
        elif value_type == 'boolean':
            # ブール値の終了条件を修正
            if value_buffer in ('true', 'false'):
                value_end_pos = value_buffer.rfind('true') if value_buffer == 'true' else value_buffer.rfind('false')
                if value_end_pos != -1:
                    value = value_buffer[:value_end_pos + 1]
                    value = value.strip()
                    return True, value
                else:
                    value = value_buffer
                    return True, value
        
        elif value_type == 'null':
            # nullの終了条件を修正
            if value_buffer == 'null':
                value_end_pos = value_buffer.rfind('null')
                if value_end_pos != -1:
                    value = value_buffer[:value_end_pos + 1]
                    return True, value
                else:
                    value = value_buffer
                    return True, value
        
        value = value_buffer
        return False, value
    
    def _extract_key_and_values(self, key_and_values: List[dict], key: str, value_buffer: str) -> List[dict]:
        value_type = self._determine_value_type(value_buffer)
        value_end, value = self._handle_value_end(value_type, value_buffer)
        if value_end:
            key_and_values.append({"key": key, "value": value})
        else:
            key_and_values.append({"key": key, "value": value_buffer})
        return key_and_values
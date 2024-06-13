from typing import Any, Dict, Generator, List, Optional, Tuple, Union
from ..openai.openai_chat_llm import OpenAIChatLLM
from ..gemini.gemini_chat_llm import GeminiChatLLM

class ChatLLM:
    def __init__(
        self, 
        llm_type: str = "openai", 
        model: str = "gpt-4o", 
        temperature: float = 0.8, 
        max_tokens: int = 2048, 
        tool_object: Optional[object] = None, 
        tools: Optional[List[dict]] = None, 
        system_message: str = "", 
        messages: Optional[List[dict]] = None, 
        tool_choice: str = "none"
    ):
        self.llm_type = llm_type
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tool_object = tool_object
        self.tools = tools
        self.system_message = system_message
        self.messages = messages
        self.tool_choice = tool_choice

        if llm_type == "openai":
            self.llm = OpenAIChatLLM(
                model=model, 
                temperature=temperature, 
                max_tokens=max_tokens, 
                tool_object=tool_object, 
                tools=tools, 
                system_message=system_message, 
                messages=messages, 
                tool_choice=tool_choice
            )
        elif llm_type == "gemini":
            self.llm = GeminiChatLLM(
                model=model, 
                temperature=temperature, 
                max_tokens=max_tokens, 
                tool_object=tool_object, 
                tools=tools, 
                system_message=system_message, 
                messages=messages, 
                tool_choice=tool_choice
            )
        else:
            raise ValueError(f"Unknown LLM type: {llm_type}")
        
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
        
        return self.llm.chat(
            user_input=user_input,
            file_path_list=file_path_list,
            image_detail=image_detail,
            model=model,
            system_message=system_message,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            tool_object=tool_object,
            temperature=temperature,
            max_tokens=max_tokens,
            mode=mode
        )
    
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
        
        return self.llm.stream_chat(
            user_input=user_input,
            file_path_list=file_path_list,
            image_detail=image_detail,
            model=model,
            system_message=system_message,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            tool_object=tool_object,
            temperature=temperature,
            max_tokens=max_tokens,
            mode=mode,
            json_keys=json_keys
        )
    
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
    ) -> Generator[str, None, None]:
        return self.llm.run(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            tool_object=tool_object,
            temperature=temperature,
            max_tokens=max_tokens,
            mode=mode
        )
        
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
        return self.llm.stream_run(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            tool_object=tool_object,
            temperature=temperature,
            max_tokens=max_tokens,
            mode=mode,
            json_keys=json_keys
        )
    
    def make_json(self, user_input, system_message = "You are a helpful assistant designed to output JSON."):
        return self.llm.make_json(user_input, system_message)
    
    def get_datas(self, user_input, tool_name, system_message = ""):
        return self.llm.get_datas(user_input, tool_name, system_message)
    
    def clear_chat(self):
        return self.llm.clear_chat()
    
    def create(self, messages, **kwargs):
        return self.llm.create(messages, **kwargs)
    
    def get_embedding(self, text):
        return self.llm.get_embedding(text)


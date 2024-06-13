import base64
import requests
import os
import tiktoken

class OpenAIChatHistory():
    def __init__(self, 
                 max_total_tokens, 
                 max_response_tokens, 
                 model,
                 messages=None, 
                 tools=None, 
                 initial_message_tokens=3, 
                 additional_message_tokens=4):
        
        self.model = model
        # メッセージがNoneの場合は空のリストを設定
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

        if tools is None:
            self.tools = []
        else:
            self.tools = tools

        self.initial_message_tokens = initial_message_tokens
        self.additional_message_tokens = additional_message_tokens
        self.max_total_tokens = max_total_tokens
        self.max_response_tokens = max_response_tokens
        self.messages_max_tokens = self.max_total_tokens - self.max_response_tokens + 2
        self.existing_messages_tokens = self._sum_tokens(self.messages)
        self.new_message_max_tokens = self.messages_max_tokens - self.existing_messages_tokens - self.additional_message_tokens

    def _count_tokens(self, text):
        return len(tiktoken.get_encoding("cl100k_base").encode(text))

    def _sum_tokens(self, messages):
        self.existing_messages_tokens = self.initial_message_tokens + self._count_tokens(f"{self.tools}")
        for message in messages:
            # 各メッセージのトークン数を加算
            for content in message["content"]:
                if content["type"] == "text":                  
                    self.existing_messages_tokens += self._count_tokens(content["text"]) + self.additional_message_tokens

        tokens = self.existing_messages_tokens
        # 新しいメッセージの最大トークン数を再計算
        self.new_message_max_tokens = self.messages_max_tokens - self.existing_messages_tokens - self.additional_message_tokens
        return tokens

    # テキストのトークン数が新しいメッセージの最大トークン数以下かどうかを比較するメソッド
    def _compare_tokens(self, text):
        if self._count_tokens(text) <= self.new_message_max_tokens:
            return True
        else:
            return False

    # メッセージを調整するメソッド
    def _adjust_messages(self, text):
        if self._compare_tokens(text):
            messages = self.messages
        else:
            # 余分なトークン数を計算
            extra_tokens = self._count_tokens(text) - self.new_message_max_tokens
            messages = self.messages
            processed_messages = messages.copy()
            for message in processed_messages:
                # 次のメッセージの余分なトークン数を計算
                for i, content in enumerate(message["content"]):
                    if content["type"] == "text":
                        next_extra_tokens = extra_tokens - (self._count_tokens(content["text"]) + self.additional_message_tokens)
                        if next_extra_tokens <= 0 and extra_tokens > 0:
                            # メッセージをエンコードして余分なトークンを削除
                            encoded_message = tiktoken.get_encoding("cl100k_base").encode(content["text"])
                            decoded_message = tiktoken.get_encoding("cl100k_base").decode(encoded_message)[-extra_tokens:]
                            messages[0]["content"][i]["text"] = decoded_message
                            break
                        messages.pop(0)
                        extra_tokens = next_extra_tokens
            self.messages = messages
        return messages
    
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def _make_image_list(self, image_url_or_path_list):
        image_list = []
        if image_url_or_path_list == None:
            image_url_or_path_list = []

        # only support PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif)
        for image_url_or_path in image_url_or_path_list:
            if not image_url_or_path.endswith(".png") and not image_url_or_path.endswith(".jpg") and not image_url_or_path.endswith(".jpeg") and not image_url_or_path.endswith(".jpg") and not image_url_or_path.endswith(".webp") and not image_url_or_path.endswith(".gif"):
                raise ValueError("Invalid image format")      
              
        # 1枚当たりの画像の制限は20MBまで、そうでなければエラー
        for image_url_or_path in image_url_or_path_list:
            if image_url_or_path.startswith("http"):
                image_size = requests.get(image_url_or_path).headers.get('content-length')
                if image_size == None:
                    raise ValueError("Invalid image size")
                if int(image_size) > 20000000:
                    raise ValueError("Invalid image size")
            else:
                image_size = os.path.getsize(image_url_or_path)
                if image_size > 20000000:
                    raise ValueError("Invalid image size")

        for image_url_or_path in image_url_or_path_list:
            if image_url_or_path.startswith("http"):
                image_list.append(image_url_or_path)
            else:
                base64_image = self.encode_image(image_url_or_path)
                image_data = f"data:image/jpeg;base64,{base64_image}"
                image_list.append(image_data)
        
        return image_list

    # メッセージを追加するメソッド
    def add_message(self, role, text, image_list = None, function_name = "", detail = "high", **kwargs):
        if image_list != None and self.model != "gpt-4-vision-preview":
            raise ValueError("Invalid model for image")
        if role not in ["user", "assistant", "function", "system"]:
            raise ValueError("Invalid role")
        if role == "function":
            content = [{"type": "text", "text": text}]
            image_url_list = self._make_image_list(image_list)
            for image_url in image_url_list:
                image_url = {"url": image_url, "detail": detail}
                content.append({"type": "image_url", "image_url": image_url})
            self.messages.append({'role': role, 'content': content, 'name': function_name})
        else:
            content = [{"type": "text", "text": text}]
            image_url_list = self._make_image_list(image_list)
            for image_url in image_url_list:
                image_url = {"url": image_url, "detail": detail}
                content.append({"type": "image_url", "image_url": image_url})          
            self.messages.append({'role': role, 'content': content})
        
        if role == "user" or role == "function":
            self.messages = self._adjust_messages(text)

        tokens = self._sum_tokens(self.messages)
        return tokens
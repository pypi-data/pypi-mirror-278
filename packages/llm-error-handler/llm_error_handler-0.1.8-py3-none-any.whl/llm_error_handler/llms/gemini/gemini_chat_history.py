import base64
from PIL import Image
import tiktoken
import google.ai.generativelanguage as glm

class GeminiChatHistory():
    def __init__(self, 
                 max_total_tokens, 
                 max_response_tokens, 
                 model,
                 messages=None, 
                 tools=None, 
                 initial_message_tokens=3, 
                 additional_message_tokens=4):
        
        self.model = model

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
            if type(message["parts"][0]) == str:
                for content in message["parts"]:
                    if type(content) == str:                  
                        self.existing_messages_tokens += self._count_tokens(content) + self.additional_message_tokens
        tokens = self.existing_messages_tokens
        self.new_message_max_tokens = self.messages_max_tokens - self.existing_messages_tokens - self.additional_message_tokens
        return tokens
    
    def _compare_tokens(self, text):
        if self._count_tokens(text) <= self.new_message_max_tokens:
            return True
        else:
            return False
        
    def _adjust_messages(self, text):
        if self._compare_tokens(text):
            messages = self.messages
        else:
            extra_tokens = self._count_tokens(text) - self.new_message_max_tokens
            messages = self.messages
            processed_messages = messages.copy()
            for message in processed_messages:
                for i, content in enumerate(message["content"]):
                    if content["type"] == "text":
                        next_extra_tokens = extra_tokens - (self._count_tokens(content["text"]) + self.additional_message_tokens)
                        if next_extra_tokens <= 0 and extra_tokens > 0:
                            encoded_message = tiktoken.get_encoding("cl100k_base").encode(content["text"])
                            decoded_message = tiktoken.get_encoding("cl100k_base").decode(encoded_message)[-extra_tokens:]
                            messages[0]["content"][i]["text"] = decoded_message
                            break
                        messages.pop(0)
                        extra_tokens = next_extra_tokens
            self.messages = messages
        return messages
    
    # def _encode_image(self, image_path):
    #     with open(image_path, "rb") as image_file:
    #         return base64.b64encode(image_file.read()).decode("utf-8")
        
    def _make_image_list(self, image_url_or_path_list):
        image_list = []
        if image_url_or_path_list == None:
            image_url_or_path_list = []

        # only support PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif)
        for image_url_or_path in image_url_or_path_list:
            if not image_url_or_path.endswith(".png") and not image_url_or_path.endswith(".jpeg") and not image_url_or_path.endswith(".jpg") and not image_url_or_path.endswith(".webp") and not image_url_or_path.endswith(".gif"):
                raise ValueError("Invalid image format")      
              
        # 1枚当たりの画像の制限は20MBまで、そうでなければエラー
        # for image_url_or_path in image_url_or_path_list:
        #     if image_url_or_path.startswith("http"):
        #         image_size = requests.get(image_url_or_path).headers.get('content-length')
        #         if image_size == None:
        #             raise ValueError("Invalid image size")
        #         if int(image_size) > 20000000:
        #             raise ValueError("Invalid image size")
        #     else:
        #         image_size = os.path.getsize(image_url_or_path)
        #         if image_size > 20000000:
        #             raise ValueError("Invalid image size")

        for image_url_or_path in image_url_or_path_list:
            if image_url_or_path.startswith("http"):
                # HTTP URLをローカルファイルパスに変換する処理
                # 例: "http://example.com/image.jpg" -> "/path/to/downloaded/image.jpg"
                # 実際には、URLからファイルをダウンロードし、ローカルに保存する必要があります。
                # ここではダウンロードと保存のプロセスを疑似コードで表現します。
                local_file_path = self._download_and_save_image(image_url_or_path)
                image_data = Image.open(local_file_path)
                image_list.append(image_data)
            else:
                local_file_path = image_url_or_path
                image_data = Image.open(local_file_path)
                image_list.append(image_data)
    
        return image_list
        
    def _download_and_save_image(self, image_url):
        import requests
        from pathlib import Path
        import tempfile
        import shutil

        # 一時ファイルのディレクトリを作成
        temp_dir = tempfile.mkdtemp()
        # URLからファイル名を抽出
        filename = Path(image_url).name
        # 保存先のパスを設定
        local_file_path = Path(temp_dir) / filename

        # 画像をダウンロード
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
        else:
            raise Exception(f"画像のダウンロードに失敗しました。ステータスコード: {response.status_code}")

        return str(local_file_path)

    def add_message(self, role, text, image_list = None, function_name = "", **kwargs):
        if image_list != None and self.model != "gemini-pro-vision":
            raise ValueError("Invalid model for image")
        if role not in ["user", "assistant", "function", "system", "model"]:
            raise ValueError("Invalid role")

        if role == "function":
            self.messages({'role': 'user', 'parts':[f"result:\n{function_name}: {text}"]})
        else:
            if role == "system":
                role = "user"
            elif role == "assistant":
                role = "model"
            content = [text]
            image_url_list = self._make_image_list(image_list)
            for image_url in image_url_list:
                content.append(image_url)
            self.messages.append({'role': role, 'parts': content})
        
        if role == "user" or role == "function":
            self.messages = self._adjust_messages(text)

        tokens = self._sum_tokens(self.messages)
        return tokens
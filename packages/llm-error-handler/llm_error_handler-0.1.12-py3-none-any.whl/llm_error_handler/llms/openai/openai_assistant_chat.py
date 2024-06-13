import os
import json
import time
from openai import OpenAI

class OpenAIAssistantChat:
    def __init__(self, assistant_id = "", update_assistant = False, instructions = "", name = "", tools = None, tools_object = None, model = "gpt-3.5-turbo", file_ids = None):
        self.client = OpenAI()
        self.threads = self.client.beta.threads
        self.thread = self.threads.create()
        if tools == None:
            tools = []
        if file_ids == None:
            file_ids = []
        if tools_object != None:
            self.tools_object = tools_object
        
        # assistant_idが空の場合は新規作成、update_assistants == Trueかつassistant_idが指定されている場合は更新
        if assistant_id == "":
            self.assistants = self.client.beta.assistants.create(
                instructions = instructions,
                name = name,
                tools = tools,
                model = model,
                file_ids = file_ids
            )
        else:
            self.assistants = self.client.beta.assistants.retrieve(assistant_id)
            if update_assistant == True:
                if instructions == "":
                    instructions = self.assistants.instructions
                if name == "":
                    name = self.assistants.name
                if tools == None:
                    tools = self.assistants.tools
                if model == "":
                    model = self.assistants.model
                if file_ids == None:
                    file_ids = self.assistants.file_ids
                self.assistants = self.client.beta.assistants.update(
                    assistant_id,
                    instructions = instructions,
                    name = name,
                    tools = tools,
                    model = model,
                    file_ids = file_ids
                )
        
        self.assistant_id = self.assistants.id

        # file_idsが指定されている場合は、code_interpreterかretrievalが指定されているか確認
        for tool in self.assistants.tools:
            if tool.type not in ["code_interpreter", "retrieval"] and file_ids != []:
                raise ValueError(f"file_ids can only be specified when code_interpreter or retrieval is specified in tools. {tool.type} is specified in tools.")

    # ツールを実行するメソッド
    def _execute_tool_call(self, name, arguments):
        tool_names = [f.function.name for f in self.assistants.tools]
        arguments = json.loads(arguments)

        # 関数名がリストに存在するか確認
        if name in tool_names:
            # 関数を取得
            tool = getattr(self.tools_object, name)
            if callable(tool):
                results = tool(**arguments)
            else:
                results = f"Error: {name} is not a function"
        else:
            results = f"Error: function {name} does not exist"

        return results

    # 返ってきたJSONデータを整形するメソッド
    def _get_run_steps_contents(self, run_steps_data_list):
        run_steps_list = []
        for run_steps_data in run_steps_data_list:
            run_step_dict = {}
            if run_steps_data.step_details.type == "tool_calls":
                run_step_dict["type"] = "tool_calls"
                run_step_dict["tool_calls"] = []
                tool_calls = run_steps_data.step_details.tool_calls
                for tool in tool_calls:
                    tool_dict = {}
                    tool_dict["type"] = tool.type
                    if tool.type == "code_interpreter":
                        tool_dict["code"] = tool.code_interpreter.input
                        tool_dict["outputs"] = []
                        outputs = tool.code_interpreter.outputs
                        for output in outputs:
                            output_dict = {}
                            output_dict["type"] = output.type
                            if output.type == "logs":
                                output_dict["logs"] = output.logs
                            elif output.type == "image":
                                output_dict["image_id"] = output.image.file_id
                            else:
                                output_dict["type"] = "exception"
                                print(f"Exception_code_interpreter_output: {output}")
                            tool_dict["outputs"].append(output_dict)
                    elif tool.type == "retrieval":
                        tool_dict["retrieval"] = tool.retrieval
                    elif tool.type == "function":
                        tool_dict["function"] = tool.function
                        tool_dict["results"] = tool.function.output

                    run_step_dict["tool_calls"].append(tool_dict)
                    
            elif run_steps_data.step_details.type == "message_creation":
                run_step_dict["type"] = "message"
                run_step_dict["message"] = []
                message_id = run_steps_data.step_details.message_creation.message_id
                message = self.threads.messages.retrieve(
                    message_id=message_id,
                    thread_id=self.thread.id,
                )
                message_contents = message.content
                for message_content in message_contents:
                    message_content_dict = {}
                    message_content_dict["type"] = message_content.type
                    if message_content.type == "image_file":
                        message_content_dict["image_id"] = message_content.image_file.file_id
                    elif message_content.type == "text":
                        message_content_dict["text"] = message_content.text.value
                        message_content_dict["annotations"] = []
                        message_content_text_annotations = message_content.text.annotations
                        for annotation in message_content_text_annotations:
                            annotation_dict = {}
                            annotation_dict["type"] = annotation.type
                            if annotation.type == "file_path":
                                annotation_dict["file_name"] = annotation.text
                                annotation_dict["file_id"] = annotation.file_path.file_id
                            else:
                                annotation_dict["type"] = "exception"
                                print(f"Exception_annotation: {annotation}")
                            message_content_dict["annotations"].append(annotation_dict)
                    else:
                        run_step_dict["message"]["type"] = "exception"
                        print(f"Exception_message_content: {message_content}")
                    run_step_dict["message"].append(message_content_dict)
            
            else:
                run_step_dict["type"] = "exception"
                print(f"Exception_run_step: {run_steps_data.step_details}")
            
            run_steps_list.append(run_step_dict)
        
        return run_steps_list
    
    # ファイルをアップロードするメソッド
    def _upload_file(self, file):
        # ファイルサイズが512MBを超えていないか確認
        if os.path.getsize(file) > 512 * 1024 * 1024:
            raise ValueError(f"File size exceeds 512MB: {file}")
        file = self.client.files.create(
            file=open(file, "rb"),
            purpose = "assistants"
        )
        return file
    
    # ファイルIDを取得するメソッド
    def _get_file_ids(self, file_path_list):
        file_ids = []
        for file in file_path_list:
            file = self._upload_file(file)
            file_ids.append(file.id)
        
        return file_ids
    
    # ファイルの拡張子がサポートされているか確認するメソッド
    def _judge_supported_file_or_not(self, file_path_list):
        retrieval = False
        code_interpreter = False
        for tool in self.assistants.tools:
            if tool.type == "code_interpreter":
                code_interpreter = True 
            elif tool.type == "retrieval":
                retrieval = True
            else:
                continue
        # それぞれのサポートファイルリスト
        if retrieval == True:
            supported_file_list = [".c", ".cpp", ".docx", ".html", ".java", ".json", ".md", ".pdf", ".php", ".pptx", ".py", ".rb", ".tex", ".txt"]
        elif code_interpreter == True and retrieval == False:
            supported_file_list = [".c", ".cpp", ".csv", ".docx", ".html", ".java", ".json", ".md", ".pdf", ".php", ".pptx", ".py", ".rb", ".tex", ".txt", ".css", ".jpeg", ".jpg", ".js", ".gif", ".png", ".tar", ".ts", ".xlsx", ".xml", ".zip"]
        else:
            supported_file_list = []

        # サポートされていないファイルがあればエラー
        for file in file_path_list:
            if os.path.splitext(file)[1] not in supported_file_list:
                raise ValueError(f"Unsupported file type: {os.path.splitext(file)[1]}. Only {supported_file_list} are supported.")

    def get_chat_contents(self, user_input, file_path_list = None):
        if file_path_list != None:
            file_ids = self._get_file_ids(file_path_list)
            self._judge_supported_file_or_not(file_path_list)
            
            messages = self.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=user_input,
                file_ids = file_ids
            )

        else:
            messages = self.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=user_input
            )

        run = self.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id
        )

        list_number = 0
        action_is_done = False
        while True:
            run = self.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            run_steps = self.threads.runs.steps.list(
                thread_id=self.thread.id,
                run_id=run.id
            )

            run_steps_data_list = run_steps.data.copy()

            while len(run_steps_data_list) > list_number:
                run_step_status = run_steps_data_list[list_number].status
                if run_step_status == "completed":
                    reversed_run_steps_data_list = run_steps.data.copy()
                    reversed_run_steps_data_list.reverse()
                    run_steps_list = self._get_run_steps_contents(reversed_run_steps_data_list)
                    yield run_steps_list[list_number]
                    list_number += 1
                else:
                    break

            if run.status == "completed":
                # print("run completed")
                break
            elif run.status == "failed":
                raise ValueError("run failed")
                # print("run failed")
                break
            elif run.status == "in_progress":
                # print("run in_progress")
                time.sleep(0.2)
                continue
            elif run.status == "requires_action":
                # print("run requires_action")
                if action_is_done == False:
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    for tool in tool_calls:
                        tool_outputs = []
                        if tool.type == "function":
                            name = tool.function.name
                            arguments = tool.function.arguments
                            id = tool.id
                            output = self._execute_tool_call(name, arguments)
                            outputs = {"tool_call_id": id, "output": output}
                        tool_outputs.append(outputs)

                    run = self.threads.runs.submit_tool_outputs(
                        thread_id=self.thread.id,
                        run_id=run.id,
                        tool_outputs = tool_outputs
                    )
                    time.sleep(0.2)
                    action_is_done = True
                continue
            else:
                print(run.status)
                time.sleep(0.2)
                continue

    def chat(self, user_input, file_path_list = None):
        chat_generater = self.get_chat_contents(user_input, file_path_list)
        for chat_response in chat_generater:
            if chat_response["type"] == "message":
                for message in chat_response["message"]:
                    if message["type"] == "text":
                        yield "text", message["text"]
                        for annotation in message["annotations"]:
                            if annotation["type"] == "file_path":
                                yield "file", annotation["file_id"]
                    elif message["type"] == "image_file":
                        yield "image", message["image_id"]
                    else:
                        print(chat_response["message"])
            elif chat_response["type"] == "tool_calls":
                for tool in chat_response["tool_calls"]:
                    if tool["type"] == "code_interpreter":
                        yield "code", tool["code"]
                        for output in tool["outputs"]:
                            if output["type"] == "logs":
                                yield "output", output["logs"]
                            else:
                                print(output)
                    elif tool["type"] == "retrieval":
                        yield "retrieval", tool["retrieval"]
                    elif tool["type"] == "function":
                        yield "function", tool["function"]
                        yield "results", tool["results"]
            else:
                print(chat_response)
    
    def get_file(self, file_id, save_path):
        file_content = self.client.files.with_raw_response.retrieve_content(file_id).content
        mnt_file_name = self.client.files.retrieve(file_id = file_id).filename
        file_name = os.path.basename(mnt_file_name)
        print(f"file_name: {file_name}")
        file_path = os.path.join(save_path, file_name)
        print(f"file_path: {file_path}")
        with open(f"{file_path}", "wb") as f:
            f.write(file_content) 

    def get_image(self, file_id, save_path):
        file_content = self.client.files.with_raw_response.retrieve_content(file_id).content
        mnt_file_name = self.client.files.retrieve(file_id = file_id).filename
        mnt_file_name += ".png"
        file_name = os.path.basename(mnt_file_name)
        print(f"file_name: {file_name}")
        file_path = os.path.join(save_path, file_name)
        print(f"file_path: {file_path}")
        with open(f"{file_path}", "wb") as f:
            f.write(file_content)
                
# if __name__ == "__main__":
#     assistant_id = "asst_xEaHEL81ugy6m61IxbgJqmQM"
#     current_script_path = os.path.abspath(__file__)
#     current_directory = os.path.dirname(current_script_path)
#     target_file_path = os.path.join(current_directory, "tools", "tools.json")

#     with open(target_file_path, "r", encoding='utf-8') as f:
#         tools = json.load(f)

#     chat = OpenAIAssistantChat(assistant_id, update_assistant = True, instructions = "足し算を指示されたら実行します。", name = "足し算チャット", tools = tools, tools_object = Tools(), model = "gpt-4-1106-preview")
#     while True:
#         user_input = input("User:")
#         # ファイルパスはカンマ区切りで入力、"で囲まれていても可
#         file_path = input("File:")
#         file_path = file_path.replace('"', "")
#         file_path_list = file_path.split(",")

#         desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

#         if file_path_list == [""]:
#             chat_generater = chat.chat(user_input)
#         else:
#             chat_generater = chat.chat(user_input, file_path_list)

#         for key, value in chat_generater:
#             if key == "text":
#                 print("AI:")
#                 print(value)
#             elif key == "file":
#                 print("ファイルを保存中...")
#                 chat.get_file(value, desktop_path)
#             elif key == "image":
#                 print("画像を保存中...")
#                 chat.get_image(value, desktop_path)
#             elif key == "code":
#                 print("コード実行中...")
#                 print(value)
#             elif key == "output":
#                 print("コード実行結果:")
#                 print(value)
#             elif key == "retrieval":
#                 print("ファイル読み込み中...")
#             elif key == "function":
#                 continue
#             elif key == "results":
#                 continue
#             else:
#                 continue


        # if file_path_list == [""]:
        #     chat_generater = chat.get_chat_contents(user_input)
        # else:
        #     chat_generater = chat.get_chat_contents(user_input, file_path_list)
        
        # for chat_response in chat_generater:
        #     if chat_response["type"] == "message":
        #         for message in chat_response["message"]:
        #             if message["type"] == "text":
        #                 print(message["text"])
        #                 for annotation in message["annotations"]:
        #                     if annotation["type"] == "file_path":
        #                         chat.get_file(annotation["file_id"], desktop_path)
        #             elif message["type"] == "image_file":
        #                 chat.get_image(message["image_id"], desktop_path)
        #     elif chat_response["type"] == "tool_calls":
        #         for tool in chat_response["tool_calls"]:
        #             if tool["type"] == "code_interpreter":
        #                 print(tool["code"])
        #                 for output in tool["outputs"]:
        #                     if output["type"] == "logs":
        #                         continue
        #                     print(output["logs"])
        #             elif tool["type"] == "retrieval":
        #                 print("ファイル読み込み中...")
        #             elif tool["type"] == "function":
        #                 print(tool["function"])
        #                 print(tool["results"])
        #     else:
        #         print(chat_response)

        
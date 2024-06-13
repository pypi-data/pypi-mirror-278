import logging
import os
import traceback
import inspect
import sys  # sysモジュールをインポート
from .llms.all_llms.chat_llm import ChatLLM
from inspect import getsource

logger = logging.getLogger('LLM_ERROR_HANDLING')
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 実行中のスクリプトのディレクトリを取得
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# ファイルハンドラーを追加、ログファイルの保存先を動的に設定
file_handler = logging.FileHandler(os.path.join(base_dir, 'llm_error_handling.log'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def trace_calls(frame, event, arg):
    if event == 'call':
        return trace_lines
    return None

def trace_lines(frame, event, arg):
    if event == 'line':
        # ローカル変数を記録
        frame.f_locals['local_vars_snapshot'] = frame.f_locals.copy()
    return trace_lines

def handle_error(e: Exception, func, args, kwargs):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "prompt/error_handling_prompt.txt"), "r", encoding='utf-8') as f:
        system_message = f.read()
    llm = ChatLLM(system_message=system_message)
    all_error_logs = ""

    # トレースバックから不要な情報を除外
    tb = traceback.extract_tb(e.__traceback__)
    filtered_tb = [frame for frame in tb if 'error_handling.py' not in frame.filename and '/lib/python' not in frame.filename]
    traceback_log = ''.join(traceback.format_list(filtered_tb))
    
    # トレースバック情報をログに追加
    all_error_logs += f"Error occurred in {func.__name__}:\n"
    all_error_logs += traceback_log + "\n"

    try:
        source_code = getsource(func)
        all_error_logs += f"Source code of {func.__name__}:\n{source_code}\n"
    except Exception as source_error:
        all_error_logs += f"Error retrieving source code: {source_error}\n"

    all_error_logs += "Contents of the variables shown up to the point of the error:\n"
    for key, value in args.items():
        log = f"{key} ({type(value)}): {value}"
        all_error_logs += log + "\n"
    for key, value in kwargs.items():
        log = f"{key} ({type(value)}): {value}"
        all_error_logs += log + "\n"

    try:
        response = llm.chat(all_error_logs)
        all_error_logs += "\n" + response + "\n"
    except Exception as llm_error:
        all_error_logs += f"Error in LLM response: {llm_error}\n"
    logger.error(all_error_logs)
    raise RuntimeError(all_error_logs)

def llm_error_handler(func):
    def wrapper(*args, **kwargs):
        sys.settrace(trace_calls)  # トレースを開始
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # 例外発生時に最後に記録されたローカル変数を取得
            local_vars = sys._getframe().f_locals['local_vars_snapshot']
            handle_error(e, func, local_vars)
        finally:
            sys.settrace(None)  # トレースを停止
    return wrapper
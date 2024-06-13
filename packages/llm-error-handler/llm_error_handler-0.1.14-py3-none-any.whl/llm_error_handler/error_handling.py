import logging
import os
import traceback
import inspect
from .llms.all_llms.chat_llm import ChatLLM
from inspect import getsource

logger = logging.getLogger('LLM_ERROR_HANDLING')
logger.setLevel(logging.ERROR)
logger.propagate = False 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ファイルハンドラーを追加
file_handler = logging.FileHandler('llm_error_handling.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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
    func_sig = inspect.signature(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            bound_args = func_sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            handle_error(e, func, bound_args.arguments, kwargs)
    return wrapper


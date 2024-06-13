import json
import re
from typing import Generator, Tuple, List, Optional

def create_key_patterns(keys: List[str]) -> dict:
    return {key: re.compile(rf'"{key}"\s*:\s*') for key in keys}

def detect_json_start(token: str, in_json: bool) -> bool:
    return in_json or '{' in token

def detect_key(buffer: List[str], key_patterns: dict) -> Tuple[Optional[str], List[str]]:
    json_fragment = ''.join(buffer)
    for key, pattern in key_patterns.items():
        match = pattern.search(json_fragment)
        if match:
            return key, buffer[match.end():]
    return None, buffer

def determine_value_type(token: str) -> Tuple[Optional[str], bool]:
    stripped_token = token.strip()
    if stripped_token.startswith('"'):
        return 'string'
    elif stripped_token.isdigit() or stripped_token == '-':
        return 'number'
    elif stripped_token.startswith('{'):
        return 'object'
    elif stripped_token.startswith('['):
        return 'array'
    elif stripped_token in ('true', 'false'):
        return 'boolean'
    elif stripped_token == 'null':
        return 'null'
    return None

def handle_value_end(value_type: str, value_buffer: List[str]) -> Tuple[bool, int, int]:
    on_going_value = "".join(value_buffer).strip()
    
    if value_type == 'string':
        # 文字列がエスケープされていないダブルクォートで終了するかを判定
        in_string = False
        for i, char in enumerate(on_going_value):
            if char == '"' and (i == 0 or on_going_value[i - 1] != '\\'):
                in_string = not in_string
        if not in_string:
            return True
    
    elif value_type == 'number':
        # 数値の終了条件を修正
        if re.match(r'^-?\d+(\.\d+)?([eE][+-]?\d+)?$', on_going_value):
            return True
    
    elif value_type == 'object':
        # オブジェクトの終了条件を修正
        start_brace_count, end_brace_count = 0, 0
        start_brace_count += on_going_value.count('{')
        end_brace_count += on_going_value.count('}')
        brace_count = start_brace_count - end_brace_count
        if brace_count == 0:
            return True
    
    elif value_type == 'array':
        # 配列の終了条件を修正
        start_bracket_count, end_bracket_count = 0, 0
        start_bracket_count += on_going_value.count('[')
        end_bracket_count += on_going_value.count(']')
        bracked_count = start_bracket_count - end_bracket_count
        if bracked_count == 0:
            return True
    
    elif value_type == 'boolean':
        # ブール値の終了条件を修正
        if on_going_value in ('true', 'false'):
            return True
    
    elif value_type == 'null':
        # nullの終了条件を修正
        if on_going_value == 'null':
            return True
    
    return False

def process_value(current_key: str, value_type: str, value_buffer: List[str], first_value_token: bool, last_value_token: bool) -> Generator[Tuple[str, str], None, None]:
    if value_type == "string":
        if first_value_token:
            yield current_key, value_buffer[0].strip('"')
        elif last_value_token:
            yield current_key, re.sub(r'"[^"]*$', '', value_buffer[-1])
        else:
            yield current_key, value_buffer[-1]
    elif value_type == "number":
        if not last_value_token:
            yield current_key, value_buffer[-1].strip()
        else:
            yield current_key, value_buffer[-1].strip(',')
    elif value_type == "object":
        if not last_value_token:
            yield current_key, value_buffer[-1].strip()
        else:
            yield current_key, re.sub(r'}.*$', '}', value_buffer[-1], flags=re.DOTALL)
    elif value_type == "array":
        if not last_value_token:
            yield current_key, value_buffer[-1].strip()
        else:
            yield current_key, re.sub(r'].*$', ']', value_buffer[-1], flags=re.DOTALL)
    elif value_type == "boolean":
        if not last_value_token:
            yield current_key, value_buffer[-1].strip()
        else:
            yield current_key, value_buffer[-1].strip(',')
    elif value_type == "null":
        if not last_value_token:
            yield current_key, value_buffer[-1].strip()
        else:
            yield current_key, value_buffer[-1].strip(',')

def stream_json_values(tokens: Generator[str, None, None], *keys: str) -> Generator[Tuple[str, str], None, None]:
    buffer: List[str] = []
    in_json: bool = False
    current_key: Optional[str] = None
    previous_key: Optional[str] = None
    value_buffer: List[str] = []
    value_type: Optional[str] = None
    first_value_token: bool = True
    last_value_token: bool = False

    key_patterns = create_key_patterns(keys)
    
    def reset_state():
        nonlocal current_key, value_type, in_json, buffer
        value_buffer.clear()
        current_key = None
        value_type = None
        on_going_json = "".join(buffer).strip()
        start_brace_count = on_going_json.count('{')
        end_brace_count = on_going_json.count('}')
        in_json = start_brace_count > end_brace_count

    for token in tokens:
        previous_key = current_key
        in_json = detect_json_start(token, in_json)
        
        if in_json:
            buffer.append(token)
        
        if not current_key and in_json:
            current_key, value_buffer = detect_key(buffer, key_patterns)
            if current_key and previous_key != current_key:
                value_buffer.clear()
            continue
        
        if current_key:
            if not value_type and token.strip():
                value_type = determine_value_type(token)
                first_value_token = True
            
            if value_type:
                value_buffer.append(token)
                last_value_token = handle_value_end(value_type, value_buffer)
                yield from process_value(current_key, value_type, value_buffer, first_value_token, last_value_token)
                first_value_token = False
                if last_value_token:
                    key_patterns.pop(current_key)
                    reset_state()
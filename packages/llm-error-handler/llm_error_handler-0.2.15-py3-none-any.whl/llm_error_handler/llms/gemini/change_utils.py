def change_message_for_gemini(message):
    from PIL import Image
    role_mapping = {'system': 'user', 'assistant': 'model', 'user': 'user', 'model': 'model'}
    return {
        'role': role_mapping.get(message['role'], message['role']), 
        'parts': [Image.open(content['image_url']) if 'image_url' in content else content[key] for content in message['content'] for key in content if key in ['text', 'image_url']]
    }

def change_messages_for_gemini(messages):
    """
    メッセージリスト内の各辞書のキーを変換します。
    各メッセージに対してchange_message_for_gemini関数を適用します。

    :param messages: [{'role': ..., 'content': [{'type':'text','text': ...}, {'type':'image_url','image_url': ...}, ...]}, ...] 形式のリスト
    :return: [{'role': ..., 'parts': [..., ...]}, ...] 形式のリスト
    """
    return [change_message_for_gemini(message) for message in messages]
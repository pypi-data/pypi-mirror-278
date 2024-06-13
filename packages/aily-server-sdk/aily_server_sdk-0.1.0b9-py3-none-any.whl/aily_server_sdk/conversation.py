import json
import uuid
from aily_core import action

SEND_MESSAGE_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_send_message'


def send_message(content: str) -> str:
    """
    发送一条消息。

    Args:
        content (str): 要发送的消息内容。

    Returns:
        str: message_id
    """
    idempotent_id = str(uuid.uuid4())

    content = {"content": {"widgets": [{"type": "Markup", "props": {"content": content, "resources": []}}]}}
    r = action.call_action(SEND_MESSAGE_API_NAME, {
        'idempotentID': idempotent_id,
        'message': {
            'content': json.dumps(content),
            'messageStatus': 'FINISHED',
            "builtinActions": [
                {
                    "builtinActionType": "FEEDBACK",
                    "enable": True,
                    "actionStatus": "NEUTRAL"
                }
            ]
        }
    })
    return r.get('messageID')


def update_message(message_id: str, content: str) -> bool:
    """
    更新指定ID的消息内容。

    Args:
        message_id (int): 要更新的消息ID。
        content (str): 新的消息内容。

    Returns:
        bool: 更新消息的结果。
            - True: 更新成功
            - False: 更新失败
    """
    # 实际的消息更新逻辑...
    success = True  # 假设更新成功
    return success

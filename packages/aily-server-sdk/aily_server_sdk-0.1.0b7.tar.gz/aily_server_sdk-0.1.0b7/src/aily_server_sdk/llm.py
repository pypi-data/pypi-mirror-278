from typing import List, Union, Literal, Optional, Dict, Iterable

from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam, ChatCompletionToolChoiceOptionParam
from pydantic import BaseModel

from aily_core import action

ACTION_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_llm'


class Function(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None


class MessageToolCall(BaseModel):
    id: str

    function: Function

    type: Literal["function"]


class Usage(BaseModel):
    input_tokens: int

    output_tokens: int


class Message(BaseModel):
    content: Optional[str] = None
    role: Literal["assistant", "user", "system"]

    tool_calls: Optional[List[MessageToolCall]] = None

    usage: Optional[Usage] = None


def convert_tool_type(messages):
    for message in messages:
        if 'tool_calls' in message:
            for tool_call in message['tool_calls']:
                tool_call['tool_type'] = tool_call['type']
    return messages


def chat_completion(
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[
            str,
            Literal[
                "BYOM-lite",
                "BYOM-plus",
                "BYOM-pro",
                "BYOM-max",
                "BYOM-ultra",
                "BYOM-4o",
                "3.5-Turbo",
                "3.5-Turbo-16K",
                "4-8K",
                "4-32k",
                "4-Turbo",
                "4o",
            ],
        ],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        # stream: bool = False,  # 当前并不支持
        tools: Iterable[ChatCompletionToolParam] = None,
        tool_choice: ChatCompletionToolChoiceOptionParam = "none",
        timeout: Optional[float] = None,
) -> Message:
    """
    Generates a response message based on the input messages and parameters.

    Args:
        messages: The list of input messages.
        model: The LLM model to use for generation.
        max_tokens: The maximum number of tokens to generate.
        temperature: The temperature value for generation.
        # stream: Whether to stream the response. Currently not supported.
        tools: The tools available for the model to use.
        tool_choice: The choice of tool usage. Can be "none", "auto", or "required".
        timeout: The timeout value for the API request.

    Returns:
        The generated response message.
    """
    action_data = {
        "llm_id": model,
        "chat_completion_parameters": {
            "chat_completion_messages": convert_tool_type(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
    }
    if tools is not None:
        action_data['chat_completion_parameters'].update({
            "tools": tools,
            "tool_choice": tool_choice,
        })

    res = action.call_action(
        action_api_name=ACTION_API_NAME,
        action_data=action_data,
        options={
            'timeout': timeout
        }
    )
    if res["choices"]:
        choice = res["choices"][0]
        message = choice["message"]
        content = message.get("content")
        role = message["role"]
        tool_calls = [
            MessageToolCall(
                id=tool_call["id"],
                function=Function(
                    name=tool_call["function"]["name"],
                    arguments=tool_call["function"]["arguments"],
                ),
                type="function",
            )
            for tool_call in message.get("tool_calls", [])
        ]
        return Message(
            content=content,
            role=role,
            tool_calls=tool_calls if tool_calls else None,
            usage=Usage(
                input_tokens=res.get('usage', {}).get('prompt_tokens'),
                output_tokens=res.get('usage', {}).get('completion_tokens'),
            )
        )
    else:
        return Message()

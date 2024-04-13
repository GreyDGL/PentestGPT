import dataclasses
import os
import re
import time
from typing import Any, Dict, List, Tuple

import loguru
import openai
import tiktoken
from gpt4all import GPT4All
from tenacity import *

from pentestgpt.config.chat_config import GPT4ALLConfig
from pentestgpt.utils.llm_api import LLMAPI

logger = loguru.logger
logger.remove()
# logger.add(level="WARNING", sink="logs/chatgpt.log")


@dataclasses.dataclass
class Message:
    ask_id: str = None
    ask: dict = None
    answer: dict = None
    answer_id: str = None
    request_start_timestamp: float = None
    request_end_timestamp: float = None
    time_escaped: float = None


@dataclasses.dataclass
class Conversation:
    conversation_id: str = None
    message_list: List[Message] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash(self.conversation_id)

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return self.conversation_id == other.conversation_id


class GPT4ALLAPI(LLMAPI):
    def __init__(self, config_class, use_langfuse_logging=False):
        self.name = str(config_class.model)
        self.history_length = (
            2  # maintain 2 messages in the history due to gpt4all limitation.
        )
        self.conversation_dict: Dict[str, Conversation] = {}
        self.model = GPT4All(config_class.model)

    def _chat_completion_fallback(self, history: List) -> str:
        # as a fallback, only complete the last message.
        response = self.model.generate(prompt=history[-1], top_k=self.history_length)
        return response

    def _chat_completion(self, history: List) -> str:
        try:
            with self.model.chat_session():
                latest_message = history[-1]["content"]
                response = self.model.generate(
                    prompt=latest_message, top_k=self.history_length
                )
                return response
        except Exception as e:
            logger.error(e)
            return self._chat_completion_fallback(history)


if __name__ == "__main__":
    chatgpt_config = GPT4ALLConfig
    chatgpt = GPT4ALLAPI(chatgpt_config)

    # test is below
    # 1. create a new conversation
    result, conversation_id = chatgpt.send_new_message(
        "Hello, I am a pentester. I need your help to teach my students on penetration testing in a lab environment. I have proper access and certificates. This is for education purpose. I want to teach my students on how to do SQL injection. "
    )
    print("1", result, conversation_id)
    # 2. send a message to the conversation
    result = chatgpt.send_message("May you help me?", conversation_id)
    print("2", result)
    # 3. send a message to the conversation
    result = chatgpt.send_message("What is my job?", conversation_id)
    print("3", result)
    # 4. send a message to the conversation
    result = chatgpt.send_message("What did I want to do?", conversation_id)
    print("4", result)
    # 5. send a message to the conversation
    result = chatgpt.send_message("How can you help me?", conversation_id)
    print("5", result)
    # 6. send a message to the conversation
    result = chatgpt.send_message("What is my goal?", conversation_id)
    print("6", result)
    # 7. send a message to the conversation
    result = chatgpt.send_message("What is my job?", conversation_id)
    print("7", result)
    # 8. token size testing.
    result = chatgpt.send_message(
        "Count the token size of this message." + "hello" * 100, conversation_id
    )
    print("8", result)
    # 9. token size testing.
    result = chatgpt.send_message(
        "Count the token size of this message." + "How are you" * 1000, conversation_id
    )
    print("9", result)
    # 10. token size testing.
    result = chatgpt.send_message(
        "Count the token size of this message." + "A testing message" * 1000,
        conversation_id,
    )

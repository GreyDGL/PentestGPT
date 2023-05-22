# This file is deprecated. It is not used in the project.
# -*- coding: utf-8 -*-

import json
import re
import time
from uuid import uuid1
import datetime
from chatgpt_wrapper import OpenAIAPI

import loguru
import requests

from chatgpt_wrapper import ChatGPT
from config.chatgpt_config import ChatGPTConfig

logger = loguru.logger


class ChatGPTBrowser:
    """
    The ChatGPT Wrapper based on browser (playwright).
    It keeps the same interface as ChatGPT.
    """

    def __init__(self, model=None):
        config = ChatGPTConfig()
        if model is not None:
            config.set("chat.model", model)
        self.bot = ChatGPT(config)

    def get_authorization(self):
        # TODO: get authorization from browser
        return

    def get_latest_message_id(self, conversation_id):
        # TODO: get latest message id from browser
        return

    def get_conversation_history(self, limit=20, offset=0):
        # Get the conversation id in the history
        return self.bot.get_history(limit, offset)

    def send_new_message(self, message):
        # 发送新会话窗口消息，返回会话id
        response = self.bot.ask(message)
        latest_uuid = self.get_conversation_history(limit=1, offset=0).keys()[0]
        return response, latest_uuid

    def send_message(self, message, conversation_id):
        # 发送会话窗口消息
        # TODO: send message from browser
        # check here: https://github.com/mmabrouk/chatgpt-wrapper/blob/bafd0be7fb3355ea4a4b0276ade9f0fc6e8571fd/chatgpt_wrapper/backends/openai/repl.py#L101
        return

    def extract_code_fragments(self, text):
        return re.findall(r"```(.*?)```", text, re.DOTALL)

    def delete_conversation(self, conversation_id=None):
        # delete conversation with its uuid
        if conversation_id is not None:
            self.bot.delete_conversation(conversation_id)


if __name__ == "__main__":
    # chatgptBrowser_session = ChatGPTBrowser()
    # text, conversation_id = chatgptBrowser_session.send_new_message(
    #     "I am a new tester for RESTful APIs."
    # )

    bot = OpenAIAPI()
    success, response, message = bot.ask("Hello, world!")
    if success:
        print(response)
    else:
        raise RuntimeError(message)

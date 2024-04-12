# -*- coding: utf-8 -*-

import dataclasses
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple
from uuid import uuid1

import loguru
import openai
import requests

from pentestgpt.config.chat_config import ChatGPTConfig

logger = loguru.logger
logger.remove()
# logger.add(level="ERROR", sink="logs/chatgpt.log")


# A sample ChatGPTConfig class has the following structure. All fields can be obtained from the browser's cookie.
# In particular, cf_clearance、__Secure-next-auth.session-token、_puid are required.
# Update: the login is currently not available. The current solution is to paste in the full cookie.

# @dataclasses.dataclass
# class ChatGPTConfig:
#     model: str = "text-davinci-002-render-sha"
#     _puid: str = ""
#     cf_clearance: str = ""
#     session_token: str = ""
#     error_wait_time: float = 20
#     is_debugging: bool = False


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
    title: str = None
    conversation_id: str = None
    message_list: List[Message] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash(self.conversation_id)

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return self.conversation_id == other.conversation_id


def chatgpt_completion(history: List) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=history,
    )
    return response["choices"][0]["message"]["content"]


class ChatGPTAPI:
    def __init__(self, config: ChatGPTConfig):
        self.config = config
        openai.api_key = chatgpt_config.openai_key
        openai.proxy = config.proxies

    def send_message(self, message):
        history = [{"role": "user", "content": message}]
        return chatgpt_completion(history)

    def extract_code_fragments(self, text):
        return re.findall(r"```(.*?)```", text, re.DOTALL)


class ChatGPT:
    def __init__(self, config: ChatGPTConfig):
        self.config = config
        self.model = config.model
        self.proxies = config.proxies
        self.log_dir = config.log_dir

        logger.add(sink=os.path.join(self.log_dir, "chatgpt.log"), level="ERROR")
        # self._puid = config._puid
        # self.cf_clearance = config.cf_clearance
        # self.session_token = config.session_token
        # conversation_id: message_id
        if "cookie" not in vars(self.config):
            raise Exception("Please update cookie in config/chat_config.py")
        self.conversation_dict: Dict[str, Conversation] = {}
        self.headers = {
            "Accept": "*/*",
            "Cookie": self.config.cookie,
            "User-Agent": self.config.userAgent,
        }
        self.headers["authorization"] = self.get_authorization()

    def refresh(self) -> str:
        # a workaround that refreshes the cookie from time to time with the configuration txt file.
        curl_str = Path(Path(self.config.curl_file)).read_text()
        # find the line that contain "cookie:"
        cookie_line = re.findall(r"cookie: (.*?)\n", curl_str)[0]
        valid_cookie = cookie_line.split(" ")[2:]
        # join them together
        self.headers["Cookie"] = " ".join(valid_cookie)
        self.headers["authorization"] = self.get_authorization()
        return self.headers["Cookie"]

    def get_authorization(self):
        try:
            url = "https://chat.openai.com/api/auth/session"
            r = requests.get(url, headers=self.headers, proxies=self.proxies)
            authorization = r.json()["accessToken"]
            # authorization = self.config.accessToken
            return f"Bearer {authorization}"
        except requests.exceptions.JSONDecodeError as e:
            logger.error(e)
            logger.error(
                "You encounter an error when communicating with ChatGPT. The most likely reason is that your cookie expired."
            )
            return None

    def get_latest_message_id(self, conversation_id):
        # Get continuous conversation message id
        try:
            url = f"https://chat.openai.com/backend-api/conversation/{conversation_id}"
            r = requests.get(url, headers=self.headers, proxies=self.proxies)
            return r.json()["current_node"]
        except requests.exceptions.JSONDecodeError as e:
            logger.error(e)
            logger.error(
                "You encounter an error when communicating with ChatGPT. The most likely reason is that your cookie expired."
            )
            return None

    def _parse_message_raw_output(self, response: requests.Response):
        # parse message raw output
        last_line = None
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if len(decoded_line) == 12:
                    break
                if "data:" in decoded_line:
                    last_line = decoded_line
        return json.loads(last_line[5:])

    def send_new_message(self, message, model=None, gen_title=False):
        if model is None:
            model = self.model
        # 发送新会话窗口消息，返回会话id
        logger.info("send_new_message")
        url = "https://chat.openai.com/backend-api/conversation"
        message_id = str(uuid1())
        data = {
            "action": "next",
            "messages": [
                {
                    "id": message_id,
                    "role": "user",
                    "content": {"content_type": "text", "parts": [message]},
                }
            ],
            "parent_message_id": str(uuid1()),
            "model": model,
        }
        start_time = time.time()
        message: Message = Message()
        message.ask_id = message_id
        message.ask = data
        message.request_start_timestamp = start_time
        r = requests.post(
            url, headers=self.headers, json=data, proxies=self.proxies, stream=True
        )

        if r.status_code != 200:
            # wait for 20s
            logger.error(r.text)
            return None, None

        # parsing result
        result = self._parse_message_raw_output(r)
        text = "\n".join(result["message"]["content"]["parts"])
        rsp_message_id = result["message"]["id"]
        conversation_id = result["conversation_id"]
        answer_id = result["message"]["id"]

        end_time = time.time()
        message.answer_id = answer_id
        message.answer = result
        message.request_end_timestamp = end_time
        message.time_escaped = end_time - start_time
        conversation: Conversation = Conversation()
        conversation.conversation_id = conversation_id
        conversation.message_list.append(message)

        if gen_title:
            title = self.gen_conversation_title(conversation_id, rsp_message_id)
            conversation.title = title

        self.conversation_dict[conversation_id] = conversation

        return text, conversation_id

    def send_message(self, message, conversation_id):
        # Send message to specific conversation
        logger.info("send_message")
        url = "https://chat.openai.com/backend-api/conversation"

        # get message from id
        if conversation_id not in self.conversation_dict:
            logger.info(f"conversation_id: {conversation_id}")
            message_id = self.get_latest_message_id(conversation_id)
            logger.info(f"message_id: {message_id}")
        else:
            message_id = (
                self.conversation_dict[conversation_id].message_list[-1].answer_id
            )

        new_message_id = str(uuid1())
        data = {
            "action": "next",
            "messages": [
                {
                    "id": new_message_id,
                    "role": "user",
                    "content": {"content_type": "text", "parts": [message]},
                }
            ],
            "conversation_id": conversation_id,
            "parent_message_id": message_id,
            "model": self.model,
        }

        start_time = time.time()
        message: Message = Message()
        message.ask_id = new_message_id
        message.ask = data
        message.request_start_timestamp = start_time

        r = requests.post(
            url, headers=self.headers, json=data, proxies=self.proxies, stream=True
        )
        if r.status_code != 200:
            # 发送消息阻塞时等待20秒从新发送
            logger.warning(f"chatgpt failed: {r.text}")
            return None, None
            # parsing result

        result = self._parse_message_raw_output(r)
        text = "\n".join(result["message"]["content"]["parts"])
        conversation_id = result["conversation_id"]
        answer_id = result["message"]["id"]

        end_time = time.time()
        message.answer_id = answer_id
        message.answer = result
        message.request_end_timestamp = end_time
        message.time_escaped = end_time - start_time
        # add additional logic for reloading (only for PentestGPT continue from previous sessions)
        if conversation_id not in self.conversation_dict:
            conversation: Conversation = Conversation()
            conversation.conversation_id = conversation_id
            self.conversation_dict[conversation_id] = conversation
        conversation: Conversation = self.conversation_dict[conversation_id]
        conversation.message_list.append(message)
        return text

    def get_conversation_history(self, limit=20, offset=0):
        # Get the conversation id in the history
        url = "https://chat.openai.com/backend-api/conversations"
        query_params = {
            "limit": limit,
            "offset": offset,
        }
        r = requests.get(
            url, headers=self.headers, params=query_params, proxies=self.proxies
        )
        if r.status_code == 200:
            json_data = r.json()
            return {item["id"]: item["title"] for item in json_data["items"]}
        else:
            logger.error("Failed to retrieve history")
            return None

    def get_cached_conversation(self, conversation_id: str) -> Conversation:
        return self.conversation_dict.get(conversation_id)

    def gen_conversation_title(self, conversation_id: str, rsp_message_id: str):
        # gen conversation title
        if not conversation_id:
            return
        url = f"https://chat.openai.com/backend-api/conversation/gen_title/{conversation_id}"
        data = {
            "message_id": rsp_message_id,
        }
        r = requests.post(url, headers=self.headers, json=data, proxies=self.proxies)

        if r.status_code != 200:
            return None

        title = r.json()["title"]

        logger.info(f"update conversation {conversation_id} title to {title}")
        return title

    def delete_conversation(self, conversation_id=None):
        # delete conversation with its uuid
        if not conversation_id:
            return
        url = f"https://chat.openai.com/backend-api/conversation/{conversation_id}"
        data = {
            "is_visible": False,
        }
        r = requests.patch(url, headers=self.headers, json=data, proxies=self.proxies)

        # delete conversation id locally
        if conversation_id in self.conversation_dict:
            del self.conversation_dict[conversation_id]

        if r.status_code == 200:
            return True
        logger.error("Failed to delete conversation")
        return False

    def extract_code_fragments(self, text):
        return re.findall(r"```(.*?)```", text, re.DOTALL)


if __name__ == "__main__":
    chatgpt_config = ChatGPTConfig()
    chatgpt = ChatGPT(chatgpt_config)
    text, conversation_id = chatgpt.send_new_message(
        "I am a new tester for RESTful APIs."
    )
    print(text, conversation_id)
    result = chatgpt.send_message(
        "generate: {'post': {'tags': ['pet'], 'summary': 'uploads an image', 'description': '', 'operationId': 'uploadFile', 'consumes': ['multipart/form-data'], 'produces': ['application/json'], 'parameters': [{'name': 'petId', 'in': 'path', 'description': 'ID of pet to update', 'required': True, 'type': 'integer', 'format': 'int64'}, {'name': 'additionalMetadata', 'in': 'formData', 'description': 'Additional data to pass to server', 'required': False, 'type': 'string'}, {'name': 'file', 'in': 'formData', 'description': 'file to upload', 'required': False, 'type': 'file'}], 'responses': {'200': {'description': 'successful operation', 'schema': {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'type': {'type': 'string'}, 'message': {'type': 'string'}}}}}, 'security': [{'petstore_auth': ['write:pets', 'read:pets']}]}}",
        conversation_id,
    )
    logger.info(chatgpt.extract_code_fragments(result))

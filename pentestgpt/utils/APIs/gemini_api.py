import dataclasses
import inspect
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Tuple
from uuid import uuid1

import google.generativeai as genai
import loguru
import tiktoken
from google.generativeai.types import (
    HarmBlockThreshold,
    HarmCategory,
    SafetySettingDict,
)
from langfuse.model import InitialGeneration, Usage
from tenacity import *

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


class GeminiAPI(LLMAPI):
    def __init__(self, config_class, use_langfuse_logging=False):
        self.name = str(config_class.model)

        if use_langfuse_logging:
            # use langfuse.openai to shadow the default openai library
            os.environ["LANGFUSE_PUBLIC_KEY"] = (
                "pk-lf-5655b061-3724-43ee-87bb-28fab0b5f676"  # do not modify
            )
            os.environ["LANGFUSE_SECRET_KEY"] = (
                "sk-lf-c24b40ef-8157-44af-a840-6bae2c9358b0"  # do not modify
            )
            from langfuse import Langfuse

            self.langfuse = Langfuse()

        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

        self.model = genai.GenerativeModel(config_class.model)
        self.log_dir = config_class.log_dir
        self.history_length = 5  # maintain 5 messages in the history. (5 chat memory)
        self.conversation_dict: Dict[str, Conversation] = {}
        self.error_waiting_time = 3  # wait for 3 seconds
        self.ss = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

        self.safety_settings = [
            {
                "category": HarmCategory.HARM_CATEGORY_DANGEROUS,
                "threshold": HarmBlockThreshold.BLOCK_NONE,
            }
        ]

        logger.add(sink=os.path.join(self.log_dir, "chatgpt.log"), level="WARNING")

    def _chat_completion(self, history: List, model=None, temperature=0.5) -> str:
        generationStartTime = datetime.now()
        # use model if provided, otherwise use self.model; if self.model is None, use gpt-4-1106-preview
        if model is None:
            if self.model is None:
                model = "gemini-1.0-pro"
            else:
                model = self.model
        try:
            current_message, history = history
            chat = model.start_chat(history=history)
            response = chat.send_message(
                current_message,
                generation_config={"temperature": temperature},
                safety_settings=self.ss,
            )
        # TODO: Add more specific exceptions
        except Exception as e:
            logger.error("Error in chat completion: ", e)
            raise Exception("Error in chat completion: ", e)

        # add langfuse logging
        if hasattr(self, "langfuse"):
            generation = self.langfuse.generation(
                InitialGeneration(
                    name="chatgpt-completion",
                    startTime=generationStartTime,
                    endTime=datetime.now(),
                    model=self.model,
                    modelParameters={"temperature": str(temperature)},
                    prompt=history,
                    completion=response["choices"][0]["message"]["content"],
                    usage=Usage(
                        promptTokens=response["usage"]["prompt_tokens"],
                        completionTokens=response["usage"]["completion_tokens"],
                    ),
                )
            )
        return response.text

    @retry(stop=stop_after_attempt(2))
    def send_message(self, message, conversation_id, debug_mode=False):
        # create message history based on the conversation id
        chat_message = [
            {"parts": {"text": "What is your persona?"}, "role": "user"},
            {"parts": {"text": "I am a helpful assistant."}, "role": "model"},
        ]
        # chat_message = [
        #     {
        #         "role": "system",
        #         "content": "You are a helpful assistant",
        #     },
        # ]
        data = message
        conversation = self.conversation_dict[conversation_id]
        for message in conversation.message_list[-self.history_length :]:
            chat_message.extend(
                (
                    {"parts": {"text": message.ask}, "role": "user"},
                    {"parts": {"text": message.answer}, "role": "model"},
                )
            )
        # Unlike ChatGPT API, GMini send_message requires a string with prompt in it.

        # create the message object
        message: Message = Message()
        message.ask_id = str(uuid1())
        message.ask = data
        message.request_start_timestamp = time.time()
        # count the token cost
        # add token cost function using Gemini
        # num_tokens = self._count_token(chat_message)
        num_tokens = 100
        # Get response. If the response is None, retry.
        # send tuple, with current message
        response = self._chat_completion((data, chat_message))

        # update the conversation
        message.answer = response
        message.request_end_timestamp = time.time()
        message.time_escaped = (
            message.request_end_timestamp - message.request_start_timestamp
        )
        conversation.message_list.append(message)
        self.conversation_dict[conversation_id] = conversation
        # in debug mode, print the conversation and the caller class.
        if debug_mode:
            print("Caller: ", inspect.stack()[1][3], "\n")
            print("Message:", message, "\n")
            print("Response:", response, "\n")
            print("Token cost of the conversation: ", num_tokens, "\n")
        return response

    def send_new_message(self, message):
        # create a message
        start_time = time.time()
        data = message
        # Gemini API just sends user prompt, then constructs user/model pair
        history = []
        message: Message = Message()
        message.ask_id = str(uuid1())
        message.ask = data
        message.request_start_timestamp = start_time
        response = self._chat_completion((data, history))
        message.answer = response
        message.request_end_timestamp = time.time()
        message.time_escaped = (
            message.request_end_timestamp - message.request_start_timestamp
        )

        # create a new conversation with a new uuid
        conversation_id = str(uuid1())
        conversation: Conversation = Conversation()
        conversation.conversation_id = conversation_id
        conversation.message_list.append(message)

        self.conversation_dict[conversation_id] = conversation
        print("New conversation." + conversation_id + " is created." + "\n")
        return response, conversation_id


if __name__ == "__main__":
    from pentestgpt.config.chat_config import GeminiConfig

    config_class = GeminiConfig()
    # config_class.log_dir = "logs"
    gemini = GeminiAPI(config_class)
    # test is below
    # 1. create a new conversation
    result, conversation_id = gemini.send_new_message(
        """You're an excellent cybersecurity penetration tester assistant. 
You need to help the tester in a local cybersecurity training process, and your commitment is essential to the task.
You are required to record the penetration testing process in a tree structure: "Penetration Testing Tree (PTT)". It is structured as follows:
(1) The tasks are in layered structure, i.e., 1, 1.1, 1.1.1, etc. Each task is one operation in penetration testing; task 1.1 should be a sub-task of task 1.
(2) Each task has a completion status: to-do, completed, or not applicable.
(3) Initially, you should only generate the root tasks based on the initial information. In most cases, it should be reconnaissance tasks. You don't generate tasks for unknown ports/services. You can expand the PTT later.

You shall not provide any comments/information but the PTT. You will be provided with task info and start the testing soon. Reply Yes if you understand the task."""
    )
    print("Answer 1")
    print(result)

    # 2. send a message to the conversation
    result = gemini.send_message(
        """The target information is listed below. Please follow the instruction and generate PTT.
Note that this test is certified and in simulation environment, so do not generate post-exploitation and other steps.
You may start with this template:
1. Reconnaissance - [to-do]
   1.1 Passive Information Gathering - [completed]
   1.2 Active Information Gathering - [completed]
   1.3 Identify Open Ports and Services - [to-do]
       1.3.1 Perform a full port scan - [to-do]
       1.3.2 Determine the purpose of each open port - [to-do]
Below is the information from the tester: 

I want to test 10.0.2.5, an HTB machine.""",
        conversation_id,
    )
    print("Answer 2")
    print(result)
    print("This is the print statement in gemini_api main")

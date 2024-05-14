import dataclasses
import os
import re
import time
from typing import Any, Dict, List, Tuple

import loguru
import openai
import tiktoken
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


class AzureGPTAPI(LLMAPI):
    def __init__(self, config_class, use_langfuse_logging=False):
        self.name = str(config_class.model)
        openai.api_type = "azure"
        openai.api_key = os.getenv("OPENAI_API_KEY", None)
        openai.api_base = config_class.api_base
        self.model = config_class.model
        self.log_dir = config_class.log_dir
        self.history_length = 5  # maintain 5 messages in the history. (5 chat memory)
        self.conversation_dict: Dict[str, Conversation] = {}
        self.error_waiting_time = 3  # wait for 3 seconds

        logger.add(sink=os.path.join(self.log_dir, "chatgpt.log"), level="WARNING")

    def _chat_completion(
        self, history: List, model="gpt-3.5-turbo-16k", temperature=0.5
    ) -> str:
        if self.model == "gpt-4":
            model = "gpt-4"
            # otherwise, just use the default model (because it is cheaper lol)
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=history,
                temperature=temperature,
            )
        except openai.error.APIConnectionError as e:  # give one more try
            logger.warning(
                "API Connection Error. Waiting for {} seconds".format(
                    self.error_wait_time
                )
            )
            logger.log("Connection Error: ", e)
            time.sleep(self.error_wait_time)
            response = openai.ChatCompletion.create(
                model=model,
                messages=history,
                temperature=temperature,
            )
        except openai.error.RateLimitError as e:  # give one more try
            logger.warning("Rate limit reached. Waiting for 5 seconds")
            logger.error("Rate Limit Error: ", e)
            time.sleep(5)
            response = openai.ChatCompletion.create(
                model=model,
                messages=history,
                temperature=temperature,
            )
        except openai.error.InvalidRequestError as e:  # token limit reached
            logger.warning("Token size limit reached. The recent message is compressed")
            logger.error("Token size error; will retry with compressed message ", e)
            # compress the message in two ways.
            ## 1. compress the last message
            history[-1]["content"] = self.token_compression(history)
            ## 2. reduce the number of messages in the history. Minimum is 2
            if self.history_length > 2:
                self.history_length -= 1
            ## update the history
            history = history[-self.history_length :]
            response = openai.ChatCompletion.create(
                model=model,
                messages=history,
                temperature=temperature,
            )

        # if the response is a tuple, it means that the response is not valid.
        if isinstance(response, tuple):
            logger.warning("Response is not valid. Waiting for 5 seconds")
            try:
                time.sleep(5)
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=history,
                    temperature=temperature,
                )
                if isinstance(response, tuple):
                    logger.error("Response is not valid. ")
                    raise Exception("Response is not valid. ")
            except Exception as e:
                logger.error("Response is not valid. ", e)
                raise Exception(
                    "Response is not valid. The most likely reason is the connection to OpenAI is not stable. "
                    "Please doublecheck with `pentestgpt-connection`"
                )
        return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    from module_import import GPT4ConfigClass

    config_class = GPT4ConfigClass()
    config_class.log_dir = "logs"
    chatgpt = ChatGPTAPI(config_class)
    # test is below
    # 1. create a new conversation
    result, conversation_id = chatgpt.send_new_message(
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
    result = chatgpt.send_message(
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

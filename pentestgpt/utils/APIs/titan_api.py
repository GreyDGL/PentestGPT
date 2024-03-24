import dataclasses
import json
import os
from typing import Any, Dict, List, Tuple

import boto3
import loguru
import tiktoken
from tenacity import *

from pentestgpt.utils.llm_api import LLMAPI

logger = loguru.logger
logger.remove()


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


class TitanAPI(LLMAPI):
    def __init__(self, config_class, use_langfuse_logging=False):
        self.name = str(config_class.model)
        self.model = config_class.model
        self.log_dir = config_class.log_dir
        self.history_length = 5  # maintain 5 messages in the history. (5 chat memory)
        self.conversation_dict: Dict[str, Conversation] = {}
        self.error_waiting_time = 3  # wait for 3 seconds
        self._bedrock_connection()

        logger.add(sink=os.path.join(self.log_dir, "titan.log"), level="WARNING")

    def _bedrock_connection(self):
        self.bedrock = boto3.client(
            "bedrock",
            "us-west-2",
            endpoint_url="https://bedrock.us-west-2.amazonaws.com",
        )

    def _chat_completion(
        self, history: List, model="amazon.titan-tg1-large", temperature=0.5
    ) -> str:
        """
        :param history: a list of strings
        :return: a string
        """
        body = json.dumps(history)
        modelId = model
        accept = "application/json"
        contentType = "application/json"
        try:
            print("body: ", body)
            print("modelId: ", modelId)
            response = self.bedrock.invoke_model(
                body=body, modelId=modelId, accept=accept, contentType=contentType
            )
            response_body = json.loads(response.get("body").read())
            response_string = response_body.get("results")[0].get("outputText")
            return response_string

        except Exception as e:
            logger.error(f"Error: {e}")
            return None


if __name__ == "__main__":
    from module_import import TitanConfigClass

    bedrock = boto3.client(
        "bedrock", "us-west-2", endpoint_url="https://bedrock.us-west-2.amazonaws.com"
    )
    output_text = bedrock.list_foundation_models()
    config_class = TitanConfigClass()
    config_class.log_dir = "logs"
    titan = TitanAPI(config_class)

    # test is below
    # 1. create a new conversation
    result, conversation_id = titan.send_new_message(
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

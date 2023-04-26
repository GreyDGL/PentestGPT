import loguru
import sys

from utils.chatgpt import ChatGPT
from config.chatgpt_config import ChatGPTConfig
import requests

logger = loguru.logger

if __name__ == "__main__":
    chatgpt_config = ChatGPTConfig()
    try:
        chatgpt = ChatGPT(chatgpt_config)
        text, conversation_id = chatgpt.send_new_message(
            "Create a conversation for testing"
        )
        # print(text, conversation_id)
        print("Now you're connected. To start PentestGPT, please use <python3 main.py>")
    except requests.exceptions.JSONDecodeError:
        print("The cookie is not properly configured. Please follow README to update cookie in config/chatgpt_config.py")
        sys.exit(1)

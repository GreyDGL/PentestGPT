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
        conversations = chatgpt.get_conversation_history()
        print(conversations)
        if conversations != None:
            # print(text, conversation_id)
            print("Now you're connected. To start PentestGPT, please use <python3 main.py>")
        else:
            print("The cookie is not properly configured. Please follow README to update cookie in config/chatgpt_config.py")
    except requests.exceptions.JSONDecodeError:
        print("The cookie is not properly configured. Please follow README to update cookie in config/chatgpt_config.py")

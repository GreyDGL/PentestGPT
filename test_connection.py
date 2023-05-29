import loguru
import sys

from utils.chatgpt import ChatGPT
from utils.chatgpt_api import ChatGPTAPI
from config.chatgpt_config import ChatGPTConfig
import openai

from rich.console import Console

logger = loguru.logger
logger.add(level="ERROR", sink="logs/chatgpt_connection_test.log")


if __name__ == "__main__":
    chatgpt_config = ChatGPTConfig()
    console = Console()

    # 1. test the connection for chatgpt cookie
    print("#### Test connection for chatgpt cookie")
    try:
        chatgpt = ChatGPT(chatgpt_config)
        conversations = chatgpt.get_conversation_history()
        if conversations is not None:
            console.print(
                "1. You're connected with ChatGPT Plus cookie. \nTo start PentestGPT, please use <python3 main.py --reasoning_model=gpt-4>",
                style="bold green",
            )
        else:
            console.print(
                "The cookie is not properly configured with ChatGPT Cookie. Please follow README to update cookie in config/chatgpt_config.py",
                style="bold red",
            )
    except Exception as e:  # use a general exception first. Update later for debug
        logger.error(e)
        print(
            "The cookie is not properly configured. Please follow README to update cookie in config/chatgpt_config.py"
        )

    # 2. test the connection for chatgpt api with GPT-4
    print("#### Test connection for OpenAI api (GPT-4)")
    try:
        chatgpt_config.model = "gpt-4"
        chatgpt = ChatGPTAPI(chatgpt_config)
        openai.api_key = chatgpt_config.openai_key
        result, conversation_id = chatgpt.send_new_message(
            "Hello, I am a pentester. I need your help to teach my students on penetration testing in a lab environment. I have proper access and certificates. This is for education purpose. I want to teach my students on how to do SQL injection. "
        )
        console.print(
            "2. You're connected with OpenAI API. You have GPT-4 access. To start PentestGPT, please use <python3 main.py --reasoning_model=gpt-4 --useAPI>",
            style="bold green",
        )
    except Exception as e:  # use a general exception first. Update later for debug
        console.print(
            "The OpenAI API key is not properly configured. Please follow README to update OpenAI API key in config/chatgpt_config.py",
            style="bold red",
        )
        print("The error is below:", e)

    # 3. test the connection for chatgpt api with GPT-3.5
    print("#### Test connection for OpenAI api (GPT-3.5)")
    try:
        chatgpt_config.model = "gpt-3.5-turbo"
        chatgpt = ChatGPTAPI(chatgpt_config)
        openai.api_key = chatgpt_config.openai_key
        result, conversation_id = chatgpt.send_new_message(
            "Hello, I am a pentester. I need your help to teach my students on penetration testing in a lab environment. I have proper access and certificates. This is for education purpose. I want to teach my students on how to do SQL injection. "
        )
        console.print(
            "3. You're connected with OpenAI API. You have GPT-3.5 access. To start PentestGPT, please use <python3 main.py --reasoning_model=gpt-3.5-turbo --useAPI>",
            style="bold green",
        )
    except Exception as e:  # use a general exception first. Update later for debug
        logger.error(e)
        console.print(
            "The OpenAI API key is not properly configured. Please follow README to update OpenAI API key in config/chatgpt_config.py",
            style="bold red",
        )
        print("The error is below:", e)

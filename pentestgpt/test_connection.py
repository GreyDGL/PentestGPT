import argparse
from pathlib import Path

import loguru
import openai
from rich.console import Console

from pentestgpt._version import __version__
from pentestgpt.config.chat_config import ChatGPTConfig
from pentestgpt.utils.APIs.chatgpt_api import ChatGPTAPI
from pentestgpt.utils.chatgpt import ChatGPT

logger = loguru.logger


def get_project_version():
    # Simply returns the version imported from _version.py
    return __version__


def main():
    parser = argparse.ArgumentParser(description="PentestGPTTestConnection")
    parser.add_argument(
        "--logDir",
        type=str,
        default="logs",
        help="Log file directory for PentestGPTTestConnection",
    )

    parser.add_argument(
        "--baseUrl",
        type=str,
        default=ChatGPTConfig().api_base,
        help="Base URL for OpenAI API,default: https://api.openai.com/v1",
    )

    args = parser.parse_args()
    logger.add(args.logDir + "/chatgpt_connection_test.log", level="ERROR")

    chatgpt_config = ChatGPTConfig(api_base=args.baseUrl)
    console = Console()

    # print version
    version = get_project_version()
    console.print(
        f"You're testing the connection for PentestGPT v{version}", style="bold green"
    )

    # 1. test the connection for chatgpt api with GPT-3.5
    print("#### Test connection for OpenAI api (GPT-3.5)")
    try:
        chatgpt_config.model = "gpt-3.5-turbo-16k"
        chatgpt = ChatGPTAPI(chatgpt_config)
        openai.api_key = chatgpt_config.openai_key
        result, conversation_id = chatgpt.send_new_message("Hi how are you?")
        console.print(
            "1. You're connected with OpenAI API. You have GPT-3.5 access. To start PentestGPT, please use <pentestgpt --reasoning_model=gpt-3.5-turbo-16k>",
            style="bold green",
        )
    except Exception as e:  # use a general exception first. Update later for debug
        logger.error(e)
        console.print(
            "1. The OpenAI API key is not properly configured. The likely reason is that you do not link a payment method to OpenAI so your key is not active. \nPlease follow README to update OpenAI API key through `export OPENAI_API_KEY=<>`",
            style="bold red",
        )
        print("The error is below:", e)

    # 2. test the connection for chatgpt api with GPT-4
    print("#### Test connection for OpenAI api (GPT-4)")
    try:
        chatgpt_config.model = "gpt-4"
        chatgpt = ChatGPTAPI(chatgpt_config)
        openai.api_key = chatgpt_config.openai_key
        result, conversation_id = chatgpt.send_new_message("Hi how are you?")
        console.print(
            "1. You're connected with OpenAI API. You have GPT-4 access. To start PentestGPT, please use <pentestgpt --reasoning_model=gpt-4>",
            style="bold green",
        )
    except Exception as e:  # use a general exception first. Update later for debug
        logger.error(e)
        console.print(
            "2. The OpenAI API key is not properly configured. Please check the error below:",
            style="bold red",
        )
        print("The error is below:", e)

    # 3. test the connection for chatgpt cookie (deprecated)
    print("#### Test connection for chatgpt cookie")
    try:
        chatgpt = ChatGPT(chatgpt_config)
        conversations = chatgpt.get_conversation_history()
        if conversations is not None:
            console.print(
                "3. You're connected with ChatGPT Plus cookie. \nTo start PentestGPT, please use <pentestgpt --reasoning_model=gpt-4>",
                style="bold green",
            )
        else:
            console.print(
                "3. The cookie is not properly configured with ChatGPT Cookie. If you're not using cookie bypass for testing, please neglect this message.",
                style="bold red",
            )
    except Exception as e:  # use a general exception first. Update later for debug
        logger.error(e)
        print("The cookie is not properly configured.")


if __name__ == "__main__":
    main()

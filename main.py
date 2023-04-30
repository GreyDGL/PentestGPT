import loguru
import sys

from utils.pentest_gpt import pentestGPT

logger = loguru.logger

if __name__ == "__main__":
    pentestGPTHandler = pentestGPT(reasoning_model="gpt-4", useAPI=False)

    # you may use this one if you want to use OpenAI API (without GPT-4)
    # pentestGPTHandler = pentestGPT(reasoning_model="gpt-4", useAPI=True)

    # you may use this one if you want to use OpenAI API with GPT-4
    # pentestGPTHandler = pentestGPT(reasoning_model="gpt-4", useAPI=True)

    # configure the session
    # TODO: add param parsing
    pentestGPTHandler.main()

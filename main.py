import loguru
import sys
import argparse

from utils.pentest_gpt import pentestGPT

logger = loguru.logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PentestGPT")
    parser.add_argument("--reasoning_model", type=str, default="gpt-4")
    parser.add_argument("--useAPI", action="store_true", default=False)
    args = parser.parse_args()

    pentestGPTHandler = pentestGPT(
        reasoning_model=args.reasoning_model, useAPI=args.useAPI
    )

    # you may use this one if you want to use OpenAI API (without GPT-4)
    # pentestGPTHandler = pentestGPT(reasoning_model="gpt-3.5-turbo", useAPI=True)

    # you may use this one if you want to use OpenAI API with GPT-4
    # pentestGPTHandler = pentestGPT(reasoning_model="gpt-4", useAPI=True)

    # configure the session
    # TODO: add param parsing
    pentestGPTHandler.main()

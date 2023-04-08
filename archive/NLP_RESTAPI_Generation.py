from utils.chatgpt import ChatGPT
from config.chatgpt_config import ChatGPTConfig
import json

import loguru

logger = loguru.logger

# format: {name: {description: str, sample_curl: str, sample_response: str}}

task_prompt_0 = """
I need your help to convert natural language REST API documentation to OpenAPI 3.0 standard.
Here are the detailed requirements:
(1) I hope that the converted openapi documentation is in json format. I will give you the description for one request at a time, and you return me the corresponding json. You should handle the output with proper indent, so that I could paste all your outputs together to form a complete documentation.
(2) For each request, I'll give you a sample curl, and a request description. You should formulate the documentation based on them, especially to fill the "example" field of the request.
"""

task_prompt_1 = """
Now we start with a service called dotCMS. Please generate a header for OpenAPI 3.0 first. Take care of the indentation so that I can directly put it together with later outputs to form one API documentation.
It supports authorization token for each request. A sample curl looks like this: 
```
curl --location --request GET 'https://demo.dotcms.com/api/v1/containers/working?containerId=REPLACE_THIS_UUID' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW5AZG90Y21zLmNvbTphZG1pbg=='
```
"""

task_prompt_2 = """
Let's start now. In the following, I'll give you a sample curl, and a request description. 
"""

if __name__ == "__main__":
    code_fragments = []
    chatGPTAgent = ChatGPT(ChatGPTConfig())
    text, conversation_id = chatGPTAgent.send_new_message(task_prompt_0)
    text = chatGPTAgent.send_message(task_prompt_1, conversation_id)
    text = chatGPTAgent.send_message(task_prompt_2, conversation_id)

    # load the documentation
    with open("../outputs/container_api.json", "r") as f:
        container_api = json.load(f)
    for key, value in container_api.items():
        if key == "title":
            # TODO: get title
            pass
        elif len(value) != 0:  # is not an empty list
            title_name = key
            for item_list in value:
                description = item_list[0]
                sample_curl = item_list[1]
            # concat description and sample_curl
            ask_text = (
                "The meta function is "
                + title_name
                + "\nThe request description is:"
                + description
                + "\nThe sample curl is below: \n"
                + sample_curl
                + "\n"
            )
            # send description and curl
            response = chatGPTAgent.send_message(ask_text, conversation_id)
            # extract code fragments
            code_fragments.append(chatGPTAgent.extract_code_fragments(response))
        else:
            logger.info("No request to process.")

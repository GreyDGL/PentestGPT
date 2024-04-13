import unittest
from http.cookies import SimpleCookie
from pentestgpt.config.chat_config import ChatGPTConfig
from pentestgpt.utils.chatgpt import ChatGPT


class TestLogin(unittest.TestCase):
    chatgpt_config = ChatGPTConfig()
    chatgpt = ChatGPT(chatgpt_config)
    text, conversation_id = chatgpt.send_new_message(
        "I am a new tester for RESTful APIs."
    )
    assert text is not None


if __name__ == "__main__":
    unittest.main()

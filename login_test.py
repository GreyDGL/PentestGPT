import unittest
from http.cookies import SimpleCookie
from config.chatgpt_config import ChatGPTConfig
from utils.chatgpt import ChatGPT


def main():
    chatgpt_config = ChatGPTConfig()
    cookie_raw = chatgpt_config.cookie
    # convert cookie to dict
    cookie = SimpleCookie()
    cookie.load(cookie_raw)
    cookies = {k: v.value for k, v in cookie.items()}
    print(cookies)
    cookie_keys = list(cookies.keys())
    # for elements in cookie, test if one can be discarded
    # create a copy of the cookies
    cookies_copy = cookies.copy()
    for key in cookie_keys:
        print("Current cookie length", len(cookies_copy))
        # remove one element
        cookies_copy.pop(key)
        # create a cookie string with all the elements except the one removed
        cookie_string = "; ".join([f"{k}={v}" for k, v in cookies_copy.items()])
        # print(cookie_string)
        chatgpt_config.cookie = cookie_string
        try:
            chatgpt = ChatGPT(chatgpt_config)
            text, conversation_id = chatgpt.send_new_message(
                "I am a new tester for RESTful APIs."
            )
            result = chatgpt.send_message(
                "generate: {'post': {'tags': ['pet'], 'summary': 'uploads an image', 'description': '', 'operationId': 'uploadFile', 'consumes': ['multipart/form-data'], 'produces': ['application/json'], 'parameters': [{'name': 'petId', 'in': 'path', 'description': 'ID of pet to update', 'required': True, 'type': 'integer', 'format': 'int64'}, {'name': 'additionalMetadata', 'in': 'formData', 'description': 'Additional data to pass to server', 'required': False, 'type': 'string'}, {'name': 'file', 'in': 'formData', 'description': 'file to upload', 'required': False, 'type': 'file'}], 'responses': {'200': {'description': 'successful operation', 'schema': {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'type': {'type': 'string'}, 'message': {'type': 'string'}}}}}, 'security': [{'petstore_auth': ['write:pets', 'read:pets']}]}}",
                conversation_id,
            )
        except Exception as e:  # when error
            # add the element back
            print(e)
            cookies_copy[key] = cookies[key]

    print("final cookie string:")
    print(cookies_copy)


if __name__ == "__main__":
    main()

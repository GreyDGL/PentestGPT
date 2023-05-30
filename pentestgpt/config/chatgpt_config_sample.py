import dataclasses


@dataclasses.dataclass
class ChatGPTConfig:
    # if you're using chatGPT (not API), please use "text-davinci-002-render-sha"
    # if you're using API, you may configure based on your needs
    model: str = "text-davinci-002-render-sha"

    # set up the openai key
    openai_key = "<your openai key>"
    # set the user-agent below
    userAgent: str = "<your user agent>"
    # set cookie below
    cookie: str = "<your cookie>"

    error_wait_time: float = 20
    is_debugging: bool = False
    curl_file: str = "config/chatgpt_config_curl.txt"
    proxies: dict = dataclasses.field(
        default_factory=lambda: {
            "http": "",
            "https": "",
        }
    )

import dataclasses


@dataclasses.dataclass
class ChatGPTConfig:
    model: str = "text-davinci-002-render-sha"
    _puid: str = ""
    cf_clearance: str = ""
    session_token: str = ""
    error_wait_time: float = 20
    is_debugging: bool = False

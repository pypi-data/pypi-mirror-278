from typing import List, Callable

class PubSubInterface:
    def __init__(self, client ):
        self._client = client

    def listen(self, topics: List[str], callback: Callable[[str, str, str], None]):
        pass

    def unlisten(self, topics: List[str]):
        pass

    def send(self, topic: str, message: str):
        pass

    def close(self):
        pass

    def ping(self):
        pass

    def on_message(self, message: str):
        pass

    def on_close(self):
        pass

    def on_error(self, error: Exception):
        pass

    def on_pong(self):
        pass
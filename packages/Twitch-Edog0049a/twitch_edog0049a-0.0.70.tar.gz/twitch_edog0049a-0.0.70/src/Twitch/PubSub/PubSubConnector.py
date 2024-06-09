import json
from Twitch.WebsocketClient.WebsocketClient import WebsocketClient
from queue import Queue

class TopicTracker:
    pass

class PubSubConnector:
    def __init__(self, topics: list) -> None:
        self.messageQ: Queue = Queue()
        self._socketClient = WebsocketClient("wss://pubsub-edge.twitch.tv",
                                            self._messageConsumer, self._messageSender)
        self._socketClient.events.on(self._socketClient.EVENTENUM.CONNECTED)

    async def _messageConsumer(self, message):
        messageData = json.loads(message)

    async def _messageSender(self):
        if self.messageQ.not_empty:
            return self.messageQ.get()
        
    async def connect(self):
        self._socketClient.connect()
    
    def onConnect(self, sender, message):
        pass

import asyncio
from typing import Awaitable, Coroutine, Optional
import websockets
from websockets.client import WebSocketClientProtocol
from Twitch.EventHandler import EventHandler
from enum import Enum
class WebsocketClient:
    TIMERDEFAULT =.1
    class EVENTENUM():
        CONNECTED = 1
        DISCONNECTED = 2
        RECONNECTED = 3
        RECONNECTING = 4
        MESSAGE = 5
        MESSAGEFAIL = 6

    def __init__(self, url: str, consumer: Awaitable, producer: Awaitable, autoReconnect:bool = True, maxRetries: Optional[int] = -1) -> None:
        self.events: EventHandler = EventHandler
        self._connection: WebSocketClientProtocol = None
        self._consumer: Awaitable = consumer
        self._producer: Awaitable = producer
        self._url:str = url
        self._autoReconnect: bool = autoReconnect
        self._reconnectTimer: float = self.TIMERDEFAULT
        self._retries: int = maxRetries
        self._messageFailed: bool = False
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

    def disconnect(self):
        if self.loop.is_running():
            self.loop.stop()

    def connect(self):
        self.loop.create_task(self._connect())
        self.loop.run_forever()

    async def _connect(self):
        try:
            async with websockets.connect(self._url) as self._connection:
                self._reconnectTimer = self.TIMERDEFAULT
                self._reconnect = self._autoReconnect
                self.events.emit(self,self.EVENTENUM.CONNECTED,"connected")
                await asyncio.gather(
                    self._consumerHandler(),
                    self._producerHandler()
                    )
                await asyncio.Future()
        except websockets.ConnectionClosed as reason:
            self.events.emit(self,self.EVENTENUM.DISCONNECTED, reason)
            if self._autoReconnect:
                await self.reconnect()
        except: 
            if self._autoReconnect:
                await self.reconnect()

    async def reconnect(self) -> bool:
        triesLeft = self._retries
        while self._autoReconnect and triesLeft!=0:
            try: 
                self.events.emit(self,self.EVENTENUM.RECONNECTING)
                await asyncio.sleep(self._reconnectTimer)
                self._reconnectTimer = self._reconnectTimer * 2
                await self._connect()
                return True
            except Exception as e:
                if triesLeft > 0:
                    triesLeft -= 1
        return False        
            
    def stopReconnect(self): 
        self._autoReconnect = False
    
    def autoReconnect(self):
        self._autoReconnect = True

    async def _consumerHandler(self):
        async for message in self._connection:
            self.events.emit(self, self.EVENTENUM.MESSAGE, message)
            await self._consumer(message)
            await asyncio.sleep(0)
                
    async def _producerHandler(self):
        while True:
            message = await self._producer()
            if message is not None:
                try:
                    await self._connection.send(message)
                except websockets.ConnectionClosed:
                    if await self.reconnect():
                        while not self._connection.open: 
                            await asyncio.sleep(0)
                        await self._connection.send(message)
                    else:
                        self.events.emit(self, self.EVENTENUM.MESSAGEFAIL, message)
            await asyncio.sleep(0)

   
   

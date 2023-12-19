from channels.consumer import AsyncConsumer

class YourConsumer(AsyncConsumer):

    async def send_message(message):
        await self.send(message)

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })

    async def websocket_disconnect(self, event):
        pass

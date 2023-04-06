"controller for the bots"


class MessageSend:
    "send and store messages"

    def __init__(self):
        self.messages = []

    async def send(self, event, message):
        "send and add a message"
        await event.respond(message)
        self.messages.append(message)

    def get(self):
        "get all messages"
        return self.messages

    def clear(self):
        "clear all messages"
        self.messages = []

    def get_last(self):
        "get the last message"
        return self.messages[-1]

class Message:

    def __init__(self, sender, receiver, task, data):
        self.sender = sender
        self.receiver = receiver
        self.task = task
        self.data = data

    def to_json(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "task": self.task,
            "data": self.data
        }
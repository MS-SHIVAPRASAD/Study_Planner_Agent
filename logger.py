import json
import uuid
from datetime import datetime

class RunLogger:

    def __init__(self):
        self.run_id = str(uuid.uuid4())
        self.logs = []

    def log(self, agent, input_data, output_data):

        entry = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "input": input_data,
            "output": output_data
        }

        self.logs.append(entry)

    def get_logs(self):
        return self.logs
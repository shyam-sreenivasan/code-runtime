import requests
import json

data = {
    "file_id": "9",
    "contents": """
class TodoStatus:
    PENDING = 0
    COMPLETED = 1
    INCOMPLETE = 2
    DELETED = 3
    EXPIRED = 4

class Todo:
    def __init__(self, name, desc, deadline, status=TodoStatus.PENDING):
        self.name = name
        self.desc = desc
        self.deadline = deadline
        self.status = status

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "deadline": self.deadline,
            "status": self.status
        }
"""
}

response = requests.put(url="http://localhost:5000/projects/todo/file", data=json.dumps(data), headers={"Content-type": "application/json"})
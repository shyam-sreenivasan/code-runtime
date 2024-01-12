class TodoStatus:
    PENDING = 0
    COMPLETED = 1
    INCOMPLETE = 2
    DELETED = 3

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

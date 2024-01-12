from todo.models import Todo
from todo.collection import TodoCollection

def create(name, desc, deadline):
    t = Todo(name, desc, deadline)
    todo_id = TodoCollection.add_todo(t)
    return todo_id

def get_all():
    return TodoCollection.get_todos()

def get(todo_id):
    return TodoCollection.get_todo(todo_id)

def update(todo_id, data):
    todo = TodoCollection.get_todo(todo_id)
    for key, value in data.items():
        if hasattr(todo, key):
            setattr(todo, key, value)
    TodoCollection.update_todo(todo)

def delete(todo_id):
    todo = TodoCollection.get_todo(todo_id)
    TodoCollection.delete_todo(todo)

def clear():
    TodoCollection.clear()
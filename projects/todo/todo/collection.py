from todo.exceptions import TodoNotFound
from todo.models import TodoStatus

class TodoCollection:
    todos = []

    @staticmethod
    def get_todos():
        return TodoCollection.todos
    
    @staticmethod
    def get_todo(todo_id):
        for t in TodoCollection.todos:
            if t.id == todo_id:
                return t
        raise TodoNotFound
    
    @staticmethod
    def add_todo(todo):
        todo.id = TodoCollection.get_next_id()
        TodoCollection.todos.append(todo)
        return todo.id

    @staticmethod
    def update_todo(todo):
        for index, t in enumerate(TodoCollection.todos):
            if t.id == todo.id:
                TodoCollection.todos[index] = todo
                return 
        raise TodoNotFound

    @staticmethod
    def delete_todo(todo):
        for t in TodoCollection.todos:
            if t == todo:
                t.status = TodoStatus.DELETED
                return 
        raise TodoNotFound
    
    @staticmethod
    def get_next_id():
        if len(TodoCollection.todos) == 0:
            return 0
        return TodoCollection.todos[-1].id + 1
    
    @staticmethod
    def clear():
        TodoCollection.todos = []
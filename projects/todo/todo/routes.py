from todo import app
from flask import request
from todo import controller as ctrl
from todo.utils import get_error_response, get_sucesss_response
from todo.exceptions import TodoNotFound

@app.route('/todos', methods=['POST'])
def createtodo():
    try:
        data = request.get_json()
        name = data.get("name")
        desc = data.get("desc")
        deadline = data.get("deadline")
        todo_id = ctrl.create(name, desc, deadline)
        return get_sucesss_response(data={"id": todo_id})
    except Exception as e:
        print(e)
    return get_error_response(msg="Error")
    

@app.route('/todos', methods=['GET'])
@app.route('/todos/<todo_id>', methods=['GET'])
def get_todos(todo_id=None):
    msg = "Error"
    try:
        if todo_id is None:
            todos = ctrl.get_all()
            return get_sucesss_response(data=[todo.as_dict() for todo in todos])
        
        todo = ctrl.get(int(todo_id))
        return get_sucesss_response(data=todo.as_dict())
    except TodoNotFound:
        msg = TodoNotFound.msg
    except Exception as e:
        print(e)

    return get_error_response(msg=msg)

@app.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    msg = "Error"
    try:
        data = request.get_json()
        ctrl.update(int(todo_id), data)
        return get_sucesss_response(data=None)
    except TodoNotFound:
        msg = TodoNotFound.msg
    except Exception as e:
        print(e)

    return get_error_response(msg=msg)

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    msg = "Error"
    try:
        ctrl.delete(int(todo_id))
        return get_sucesss_response(data=None)
    except TodoNotFound:
        msg = TodoNotFound.msg
    except Exception as e:
        print(e)

    return get_error_response(msg=msg)

@app.route('/todos', methods=['DELETE'])
def clear_todos():
    msg = "Error"
    try:
        ctrl.clear()
        return get_sucesss_response(data=None)
    except TodoNotFound:
        msg = TodoNotFound.msg
    except Exception as e:
        print(e)

    return get_error_response(msg=msg)
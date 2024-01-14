from coderuntime.constants import success_response, error_response, ignore_files_like, ExecutionCodes, project_root
from coderuntime.utils import timedfunction, get_project_tree
from flask import request, jsonify
from coderuntime.execution import execute
from coderuntime.exceptions import UnsupportedRuntime
from coderuntime import app
import os
projects = None
project_tree = {}
project_path_map = {}

@app.route('/', methods=["GET"])
def home():
    return "Works"

@app.after_request
def after_request(response):
    return jsonify(response)

@app.route('/projects', methods=['GET'])
@app.route('/projects/<name>', methods=['GET'])
def get_projects(name=None):
    global projects
    try:
        if name is None:
            if projects is None:
                for item in os.listdir(project_root):
                    if os.path.isdir(os.path.join(project_root, item)):
                        projects.append(item)
            success_response["data"]["projects"] = projects
            return success_response
        
        if name.strip() == 0:
            error_response["data"]["msg"] = "Name cannot be empty"
            return error_response
        
        if name not in projects:
            error_response["data"]["msg"] = "Project not found"

        tree, path_map = get_project_tree(name, project_root, ignore_files=ignore_files_like)
        project_tree["name"] = tree
        project_path_map["name"] = path_map
        success_response["data"]["project"] = tree
        return success_response
        
    except Exception as e:
        print(e)
    error_response["data"]["msg"] = "Unknown error"

    return error_response

@app.route('/execute', methods=["POST"])
def codeexec():
    try:
        req = request.get_json()
        code = req.get('code')
        runtime = req.get('runtime')
        time_taken, result = timedfunction(execute, code, runtime)
        output, code = result

        if code == ExecutionCodes.ERROR:
            error_response["data"]["msg"] = output
            return jsonify(error_response)
        
        success_response["data"]["output"] = output
        success_response["data"]["completed_in_secs"] = f"{int(time_taken)}"
        return success_response
    except UnsupportedRuntime:
        error_response["data"]["msg"] = "Unsupported Runtime"
        return error_response
    except Exception as e:
        print(e)

    error_response["data"]["msg"] = "Unknown Error. Please try again later"
    return error_response

@app.route('/project/<project_name>/file/<file_id>', methods=['GET'])
def getfile(project_name, file_id):
    try:
        if project_name not in projects:
            error_response["data"]["msg"] = "No such project found"
            return error_response

        path_map = project_path_map[project_name]
        for item in path_map:
            if int(item['id']) == int(file_id):
                with open(item['fullpath'], 'r') as f:
                    contents = f.readlines()
                    print(contents)
                    success_response["data"] = {
                        "project_name": project_name,
                        "file_id": file_id,
                        "contents": contents 
                    }
        
                return success_response
    except Exception as e:
        print(e)

    error_response["data"]["msg"] = "Unable to get file contents"
    return error_response

@app.route('/project/<project_name>/file', methods=["PUT"])
def updatefile(project_name):
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        contents = data.get('contents')
        if project_name not in projects:
            error_response["data"]["msg"] = "No such project found"
            return error_response
        path_map = project_path_map[project_name]
        for item in path_map:
            if int(item['id']) == int(file_id):
                with open(item['fullpath'], 'w') as f:
                    f.writelines(contents)
                success_response["data"]["msg"] = "File Updated Successfully"
                return success_response
    except Exception as e:
        print(e)
    return error_response

@app.route('/project/deploy', methods=['POST'])
def deploy_project():
    return
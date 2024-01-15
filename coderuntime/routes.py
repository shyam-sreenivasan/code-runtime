from coderuntime.constants import ignore_files_like, ExecutionCodes, project_root, project_ports, PROJECT_NOT_FOUND
from coderuntime.utils import timedfunction, get_project_tree, find_process_by_port, get_projects
from flask import request
from coderuntime.execution import execute
from coderuntime.exceptions import UnsupportedRuntime
from coderuntime import app, projects
import subprocess
import traceback

project_tree = {}
project_path_map = {}
running_processes = {}


@app.route('/', methods=["GET"])
def home():
    return {"status": 100, "data": {}}

@app.route('/projects', methods=['GET'])
@app.route('/projects/<name>', methods=['GET'])
def get_projects(name=None):
    global projects
    try:
        if name is None:
            return {"status": 100, "data": {"projects": projects}}
        
        if name.strip() == 0:
            return {"status": 101, "data": {"msg": "Name cannot be empty"}}

        if name not in projects:
            return {"status": 101, "data": {"msg": PROJECT_NOT_FOUND}}
        
        tree, path_map = get_project_tree(name, project_root, ignore_files=ignore_files_like)
        project_tree[name] = tree
        project_path_map[name] = path_map
        return {"status": 100, "data": {"project": tree}}
        
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
    return {"status": 101, "data": {"msg": "Unknown error"}}

@app.route('/execute', methods=["POST"])
def codeexec():
    try:
        req = request.get_json()
        code = req.get('code')
        runtime = req.get('runtime')
        time_taken, result = timedfunction(execute, code, runtime)
        output, code = result

        if code == ExecutionCodes.ERROR:
            return {"status": 101, "data": {"msg": output}}

        return {"status": 100, "data": {"output": output, "completed_in_secs": f"{int(time_taken)}"}}
    except UnsupportedRuntime:
        return {"status": 101, "data": {"msg": "Unsupported Runtime"}}
    except Exception as e:
        print(e)

    return {"status": 101, "data": {"msg": "Unknown Error. Please try again later"}}

@app.route('/projects/<project_name>/file/<file_id>', methods=['GET'])
def getfile(project_name, file_id):
    try:
        if project_name not in projects:
            return {"status": 101, "data": {"msg": PROJECT_NOT_FOUND}}
        print(project_path_map)
        path_map = project_path_map[project_name]
        for item in path_map:
            if int(item['id']) == int(file_id):
                with open(item['path'], 'r') as f:
                    contents = f.read()
        
                return {"status": 100, "data": {
                        "project_name": project_name,
                        "file_id": file_id,
                        "contents": contents 
                    }}
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()

    return {"status": 101, "data": {"msg": "Unable to get file contents"}}

@app.route('/projects/<project_name>/file', methods=["PUT"])
def updatefile(project_name):
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        contents = data.get('contents')
        if project_name not in projects:
            return {"status": 101, "data": {"msg": PROJECT_NOT_FOUND}}
        path_map = project_path_map[project_name]
        for item in path_map:
            if int(item['id']) == int(file_id):
                with open(item['path'], 'w') as f:
                    f.write(contents)
                return {"status": 100, "data": {"msg": "File Updated Successfully"}}
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
    return {"status": 101, "data": {"msg": "Unknow Error"}}

@app.route('/projects/<project_name>/deploy', methods=['POST'])
def deploy_app(project_name):
    try:
        if project_name not in projects:
            return {"status": 101, "data": {"msg": PROJECT_NOT_FOUND}}

        existing_process = find_process_by_port(project_ports[project_name])
        if existing_process:
            existing_process.terminate()
            existing_process.wait()
            print("Existing process terminated")
        
        process = subprocess.Popen(['python', 'projects/todo/main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if find_process_by_port(project_ports[project_name]):
            running_processes[project_name] = {'process': process, 'pid': process.pid}
            return {"status": 100, "data": {"msg": "Service deployed", "url": f"http://localhost:{project_ports[project_name]}/"}}

    
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
    return {"status": 101, "data": {"msg": "Unable to deploy service"}}

@app.route("/projects/<project_name>/stop", methods=['POST'])
def stop_app(project_name):
    try:
        if project_name not in projects:
            return {"status": 101, "data": {"msg": PROJECT_NOT_FOUND}}

        existing_process = find_process_by_port(project_ports[project_name])
        if not existing_process:
            return {"status": 101, "data": {"msg": "App is not running"}}
        existing_process.terminate()
        existing_process.wait()
        running_processes.pop(project_name)
        print("Existing process terminated")
        return {"status": 100, "data": {"msg": "App terminated"}}
    except Exception as e:
        print(e)
        traceback.print_exc()
    return {"status": 101, "data": {"msg": "Unable to stop app"}}
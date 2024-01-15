supported_runtimes = ["python3.10"]
default_execution_err_msg = "An error occurred"
project_root = "./projects"

class ExecutionCodes:
    SUCCESS = 100
    ERROR = 101

success_response = {
    "status": ExecutionCodes.SUCCESS,
    "data": {
        "output": None,
        "completed_in_secs": None
    } 
    
}

error_response = {
    "status": ExecutionCodes.ERROR,
    "data": {
        "msg": None
    }
}

ignore_files_like = ["__pycache__"]
project_ports = {
    "todo": 5001
}
PROJECT_NOT_FOUND = "Project Not Found"
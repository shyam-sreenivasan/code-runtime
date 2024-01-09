supported_runtimes = ["python3.10"]
default_execution_err_msg = "An error occurred"
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
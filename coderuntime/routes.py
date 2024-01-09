from coderuntime.constants import success_response, error_response, ExecutionCodes
from coderuntime.utils import timedfunction
from flask import request, jsonify
from coderuntime.env import execute
from coderuntime.exceptions import UnsupportedRuntime
from coderuntime import app

@app.route('/', methods=["GET"])
def home():
    return "Works"

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
        return jsonify(success_response)
    except UnsupportedRuntime:
        error_response["data"]["msg"] = "Unsupported Runtime"
        return jsonify(error_response)
    except Exception as e:
        print(e)

    error_response["data"]["msg"] = "Unknown Error. Please try again later"
    return jsonify(error_response)
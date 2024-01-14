import tempfile
import subprocess
import os
from coderuntime.constants import supported_runtimes, default_execution_err_msg, ExecutionCodes
from coderuntime.exceptions import UnsupportedRuntime

def execute(code, runtime):
    if runtime not in supported_runtimes:
        raise UnsupportedRuntime
    
    err_msg = default_execution_err_msg
    result = None
    if runtime == "python3.10":
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            result = subprocess.run(['python', temp_file_path], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout, ExecutionCodes.SUCCESS
        except subprocess.TimeoutExpired:
            print("Subprocess timed out after 5 seconds.")
            err_msg = "Timed Out"
        except subprocess.CalledProcessError as e:
                print(f"Subprocess returned a non-zero exit code: {e.returncode}")
        finally:
            if temp_file_path:
                os.remove(temp_file_path)
    return err_msg if not isinstance(result, subprocess.CompletedProcess) else result.stderr, ExecutionCodes.ERROR
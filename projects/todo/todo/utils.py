from flask import jsonify

class ResponseCodes:
    SUCCESS = 100
    ERROR = 101

def get_response(status, data, msg):
    return jsonify({
        "status": status,
        "data": data,
        "msg": msg
    })

def get_sucesss_response(data, msg=None):
    return get_response(ResponseCodes.SUCCESS, data, msg)

def get_error_response(msg, data=None):
    return get_response(ResponseCodes.ERROR, data, msg)

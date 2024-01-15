import coderuntime as crt
crt.init()
crt.app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
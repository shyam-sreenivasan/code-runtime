import requests
import json
import time

runtime = "python3.10"
code = """
print("Hello")
"""
url = "http://localhost:5000/execute"

response = requests.post(url=url, json={
    "code": code,
    "runtime": runtime
})
print(json.dumps(response.json(), indent=4))
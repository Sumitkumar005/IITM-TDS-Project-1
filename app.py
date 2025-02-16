from flask import Flask, request, jsonify, Response
import os
import traceback
from agent import run_task

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_endpoint():
    task = request.args.get('task')
    if not task:
        return Response("Missing task description", status=400)
    try:
        message = run_task(task)
        return jsonify({"status": "success", "message": message})
    except ValueError as ve:
        return Response(str(ve), status=400)
    except Exception as e:
        traceback.print_exc()
        return Response("Internal Server Error: " + str(e), status=500)

@app.route('/read', methods=['GET'])
def read_endpoint():
    path = request.args.get('path')
    if not path:
        return Response("Missing file path", status=400)
    # Enforce security: only allow files within /data
    if not path.startswith("/data"):
        return Response("Access denied", status=403)
    try:
        if not os.path.exists(path):
            return Response("", status=404)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, status=200, mimetype='text/plain')
    except Exception as e:
        traceback.print_exc()
        return Response("Internal Server Error", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

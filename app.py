from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources = {r"/*": {"origins": "*"}})
data_file = "/tmp/class_album.json"

@app.route("/submit", methods = ["POST", "OPTIONS", "GET"])
def submit():
    if request.method == "GET":
        return "successfully fetched", 200
    if request.method == "OPTIONS":
        return "", 200
    
    data = request.get_json()
    name = data.get("name", "")
    tmp = {}
    if os.path.exists(data_file):
        with open(data_file, "r", encoding = "utf-8") as file:
            try:
                tmp = json.load(file)
            except:
                tmp = {}
    tmp[name] = data
    with open(data_file, "w", encoding = "utf-8") as file:
        json.dump(tmp, file)
    return jsonify({
        "status": "success",
        "message": "fetched successfully"
    }), 200

@app.route("/list", methods = ["GET"])
def list():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding = "utf-8") as file:
            data = json.load(file)
            return data, 200
    return {}, 200

@app.route("/del/<name>", methods = ["DELETE", "OPTIONS", "GET"])
def delete(name):
    if request.method == "OPTIONS":
        return "", 200
    
    if os.path.exists(data_file):
        with open(data_file, "r", encoding = "utf-8") as file:
            try:
                tmp = json.load(file)
                if name not in tmp:
                    return jsonify({
                        "status": "error",
                        "message": f"'{name}' not found"
                    }), 404
            except:
                return jsonify({
                    "status": "error",
                    "message": f"'{name}' not found"
                }), 404
    else:
        return jsonify({
            "status": "error",
            "message": f"'{name}' not found"
        }), 404
    tmp.pop(name)
    with open(data_file, "w", encoding = "utf-8") as file:
        json.dump(tmp, file)
    return jsonify({
        "status": "success",
        "message": f"deleted '{name}' successfully"
    }), 200

@app.route("/clear", methods = ["DELETE", "OPTIONS", "GET"])
def clear():
    if request.method == "OPTIONS":
        return "", 200
    
    if os.path.exists(data_file):
        with open(data_file, "w", encoding = "utf-8") as file:
            json.dump({}, file)
        return jsonify({
            "status": "success",
            "message": "deleted all data successfully"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "No data found"
        }), 404

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host = "0.0.0.0", port = port, debug = True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app, resources = {r"/*": {"origins": "*"}})

database_url = os.environ.get('DATABASE_URL')
def database(): return psycopg2.connect(database_url)

@app.route("/submit", methods = ["POST", "OPTIONS", "GET"])
def submit():
    if request.method == "GET":
        return "successfully fetched", 200
    if request.method == "OPTIONS":
        return "", 200
    
    data = request.get_json()
    name = data.get("name", "")
    con = database()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO class_album (name, data) 
        VALUES (%s, %s)
        ON CONFLICT (name) DO UPDATE SET data = EXCLUDED.data
    ''', (name, json.dumps(data)))
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        "status": "success",
        "message": "fetched successfully"
    }), 200

@app.route("/list", methods = ["GET"])
def list_all():
    con = database()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT name, data FROM class_album")
    tmp = cur.fetchall()
    cur.close()
    con.close()
    result = {}
    for i in tmp:
        result[i["name"]] = i["data"]
    return result, 200

@app.route("/del/<name>", methods = ["DELETE", "OPTIONS", "GET"])
def delete(name):
    if request.method == "OPTIONS":
        return "", 200
    
    con = database()
    cur = con.cursor()
    cur.execute("DELETE FROM class_album WHERE name = %s RETURNING name", (name,))
    tmp = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    if tmp:
        return jsonify({
            "status": "success",
            "message": f'deleted "{name}" successfully'
        }), 200
    return jsonify({
        "status": "error",
        "message": f'"{name}" not found'
    }), 404

@app.route("/clear", methods = ["DELETE", "OPTIONS", "GET"])
def clear():
    if request.method == "OPTIONS":
        return "", 200
    
    con = database()
    cur = con.cursor()
    cur.execute("DELETE FROM class_album")
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        "status": "success",
        "message": "deleted all data successfully"
    }), 200

if __name__ == "__main__":
    try:
        con = database()
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS class_album (
                name TEXT PRIMARY KEY,
                data JSONB
            )
        ''')
        con.commit()
        cur.close()
        con.close()
        print(50 * "=" + "\ndatabase connected\n" + 50 * "=")
    except Exception as err:
        print(f"database error: {err}")

    port = int(os.environ.get("PORT", 8080))
    app.run(host = "0.0.0.0", port = port, debug = True)@app.route("/list", methods = ["GET"])
def list_all():
    con = database()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT name, data FROM class_album")
    tmp = cur.fetchall()
    cur.close()
    con.close()
    result = {}
    for i in tmp:
        result[i["name"]] = i["data"]
    return result, 200

@app.route("/del/<name>", methods = ["DELETE", "OPTIONS", "GET"])
def delete(name):
    if request.method == "OPTIONS":
        return "", 200
    
    con = database()
    cur = con.cursor()
    cur.execute("DELETE FROM class_album WHERE name = %s RETURNING name", (name,))
    tmp = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    if tmp:
        return jsonify({
            "status": "success",
            "message": f'deleted "{name}" successfully'
        }), 200
    return jsonify({
        "status": "error",
        "message": f'"{name}" not found'
    }), 404

@app.route("/clear", methods = ["DELETE", "OPTIONS", "GET"])
def clear():
    if request.method == "OPTIONS":
        return "", 200
    
    con = database()
    cur = con.cursor()
    cur.execute("DELETE FROM class_album")
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        "status": "success",
        "message": "deleted all data successfully"
    }), 200

if __name__ == "__main__":
    database_url = os.environ.get('DATABASE_URL')
    try:
        con = database()
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS class_album (
                name TEXT PRIMARY KEY,
                data JSONB
            )
        ''')
        con.commit()
        cur.close()
        con.close()
        print(50 * "=" + "\ndatabase connected\n" + 50 * "=")
    except Exception as err:
        print(f"database error: {err}")
        
    port = int(os.environ.get("PORT", 8080))
    app.run(host = "0.0.0.0", port = port, debug = True)

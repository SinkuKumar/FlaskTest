from flask import Flask, jsonify
import sqlite3
import time
import os
import random

def create_db():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)")
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route("/cpu-load")
def cpu_load():
    start = time.time()
    while time.time() - start < 5:  # 5 seconds of high CPU usage
        _ = [x**2 for x in range(1000000)]
    return jsonify({"message": "CPU load completed"})

@app.route("/memory-load")
def memory_load():
    memory_hog = []
    for _ in range(50):  # Allocating large memory
        memory_hog.append(os.urandom(10**6))  # 1MB per iteration
        time.sleep(0.1)
    return jsonify({"message": "Memory load completed"})

@app.route("/db-load")
def db_load():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    for _ in range(1000):  # Insert 1000 rows
        c.execute("INSERT INTO test (data) VALUES (?)", (str(random.random()),))
    conn.commit()
    conn.close()
    return jsonify({"message": "Database load completed"})

@app.route("/")
def home():
    return jsonify({"message": "Flask Load Test App"})

if __name__ == "__main__":
    create_db()
    app.run(host="0.0.0.0", port=9000)

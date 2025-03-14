from flask import Flask, jsonify
import pyodbc
import time
import os
import random

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=master;'
        'UID=sa;'
        'PWD=Graphx@123;'
        'TrustServerCertificate=yes'
    )
    return conn

def create_db():
    conn = get_db_connection()
    conn.autocommit = True  # Enable autocommit to avoid transaction issues
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'testdb')
        CREATE DATABASE testdb;
    """)
    conn.close()
    
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=testdb;'
        'UID=sa;'
        'PWD=Graphx@123;'
        'TrustServerCertificate=yes'
    )
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='test' AND xtype='U')
        CREATE TABLE test (
            id INT IDENTITY(1,1) PRIMARY KEY,
            data NVARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route("/cpu-load")
def cpu_load():
    start = time.time()
    while time.time() - start < 5:
        _ = [x**2 for x in range(1000000)]
    return jsonify({"message": "CPU load completed"})

@app.route("/memory-load")
def memory_load():
    memory_hog = []
    for _ in range(50):
        memory_hog.append(os.urandom(10**6))
        time.sleep(0.1)
    return jsonify({"message": "Memory load completed"})

@app.route("/db-load")
def db_load():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=testdb;'
        'UID=sa;'
        'PWD=Graphx@123;'
        'TrustServerCertificate=yes'
    )
    cursor = conn.cursor()
    for _ in range(1000):
        cursor.execute("INSERT INTO test (data) VALUES (?)", (str(random.random()),))
    conn.commit()
    conn.close()
    return jsonify({"message": "Database load completed"})

@app.route("/")
def home():
    return jsonify({"message": "Flask Load Test App"})

if __name__ == "__main__":
    create_db()
    app.run(host="0.0.0.0", port=9000)

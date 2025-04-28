from flask import Flask, request, render_template
import psycopg2
import os
import socket

app = Flask(__name__)

# Supabase PostgreSQL credentials from environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_PORT = os.environ.get('DB_PORT', 5432)

# 🔥 DEBUG: Print all database environment values
print("\n=== DATABASE CONFIGURATION ===")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")
print(f"DB_PASS: {DB_PASS}")
print(f"DB_PORT: {DB_PORT}")
print("===============================\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    headers = None
    error = None
    if request.method == 'POST':
        sql = request.form['sql']
        try:
            # 🔥 DEBUG: Try resolving DB_HOST to IPv4
            print(f"Trying to resolve {DB_HOST} to IPv4 address...")
            ipv4_host = socket.gethostbyname(DB_HOST)
            print(f"Resolved IPv4 address: {ipv4_host}")

            conn = psycopg2.connect(
                host=ipv4_host,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT,
                options='-c statement_timeout=10000'
            )
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            cur.close()
            conn.close()
        except Exception as e:
            print(f"🔥 ERROR during query execution: {e}")
            error = str(e)
    return render_template('index.html', headers=headers, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)

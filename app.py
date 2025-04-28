import os
import psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

# Railway database credentials
DB_HOST = os.getenv('DB_HOST', 'your_host_from_railway')
DB_NAME = os.getenv('DB_NAME', 'your_db_name')
DB_USER = os.getenv('DB_USER', 'your_db_user')
DB_PASS = os.getenv('DB_PASS', 'your_db_password')
DB_PORT = os.getenv('DB_PORT', '5432')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

# rest of your app

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

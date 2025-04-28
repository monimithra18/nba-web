
from flask import Flask, request, render_template
import psycopg2
import os

app = Flask(__name__)

# Supabase PostgreSQL credentials from Environment Variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_PORT = os.environ.get('DB_PORT', 5432)  # Default port 5432

def run_query(sql):
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return headers, rows

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    headers = None
    error = None
    if request.method == 'POST':
        sql = request.form['sql']
        try:
            headers, result = run_query(sql)
        except Exception as e:
            error = str(e)
    return render_template('index.html', headers=headers, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)

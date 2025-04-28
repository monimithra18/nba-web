import os
import psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

# Load DB credentials from environment
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT', 5432)

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    if request.method == 'POST':
        query = request.form['query']
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query)
            if query.lower().strip().startswith('select'):
                result = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)

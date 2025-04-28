from flask import Flask, request, render_template
import psycopg2
import pandas as pd
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=os.environ.get('DB_PORT', 5432)  # default 5432
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        try:
            conn = get_db_connection()
            result = pd.read_sql_query(query, conn)
            conn.close()
        except Exception as e:
            result = str(e)
    return render_template('index.html', result=result, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

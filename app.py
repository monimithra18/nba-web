from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ''
    error = None

    if request.method == 'POST':
        query = request.form['query']
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query)
            if query.strip().lower().startswith('select'):
                results = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            error = str(e)

    return render_template('index.html', results=results, query=query, error=error)

if __name__ == '__main__':
    app.run(debug=True)

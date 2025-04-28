from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

# Supabase PostgreSQL credentials (replace with your actual values)
DB_HOST = 'db.erdhktauqqvehhhhczds.supabase.co'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = '281803'
DB_PORT = 5432

# Function to run a SQL query
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

# Home route with query input
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

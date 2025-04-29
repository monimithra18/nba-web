from flask import Flask, request, render_template
import psycopg2
import pandas as pd

app = Flask(__name__)

# Database credentials (FROM SUPABASE)
DB_HOST = "db.erdhktauqqvehhhhczds.supabase.co"
DB_NAME = "postgres"          # Default Supabase database name
DB_USER = "postgres"          # Default Supabase user
DB_PASS = "281803"
DB_PORT = "5432"              # Default port

def run_query(query):
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        sslmode="require"     # IMPORTANT for Supabase!
    )
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    output_table = None
    error_message = None

    if request.method == 'POST':
        user_query = request.form['query']
        try:
            output_table = run_query(user_query)
        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render_template('index.html', table=output_table, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Configuration for Vercel Postgres
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def redeem_coupon():
    if request.method == 'POST':
        code = request.form['code']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM coupons WHERE code = %s AND redeemed = FALSE', (code,))
        coupon = cursor.fetchone()
        if coupon:
            cursor.execute('UPDATE coupons SET redeemed = TRUE WHERE code = %s', (code,))
            conn.commit()
            conn.close()
            return render_template('redeem.html', message=f"Selamat Kamu Mendapatkan {coupon[2]}")
        else:
            conn.close()
            return render_template('redeem.html', message="Kode Kupon Tidak Valid atau Sudah Diredeem")
    return render_template('redeem.html')

if __name__ == '__main__':
    app.run()

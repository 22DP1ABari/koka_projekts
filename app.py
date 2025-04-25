from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Atver datubāzi
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, license_valid INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS results (L REAL, B REAL, H REAL, f REAL, q REAL)''')
conn.commit()

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    B, H, f = data['B'], data['H'], data['f']
    W = (B * H**2) / 6
    q = 8 * W * f / 1000  # kN/m
    cursor.execute('INSERT INTO results VALUES (?, ?, ?, ?, ?)', (data['L'], B, H, f, q))
    conn.commit()
    return jsonify({'q': q})

@app.route('/api/license', methods=['POST'])
def check_license():
    data = request.get_json()
    cursor.execute('SELECT license_valid FROM users WHERE name=? AND email=?', (data['name'], data['email']))
    result = cursor.fetchone()
    return jsonify({'valid': result[0] == 1 if result else False})

if __name__ == '__main__':
    app.run(debug=True)

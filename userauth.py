from flask import Flask, request, jsonify
import sqlite3
from fetch_balance import get_balance
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

DATABASE = 'relieflink.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"msg": "Email and password required"}), 400

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if not user:
            return jsonify({"msg": "Invalid email or password"}), 401

        if user['password'] != password:
            return jsonify({"msg": "Invalid email or password"}), 401

        public_key = user['public_key']
        balance = get_balance(public_key)

        response = {
            "name": user['name'],
            "email": user['email'],
            "city": user['city'],
            "public_key": public_key,
            "balance": balance
        }
        return jsonify(response), 200

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"msg": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Explicitly set port 8000
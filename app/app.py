import os
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "api"
    })

@app.route('/db-check')
def db_check():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("MYSQL_USER", "appuser"),
            password=os.getenv("MYSQL_PASSWORD", "secretpass"),
            database=os.getenv("MYSQL_DATABASE", "appdb")
        )
        return jsonify({"database": "connected", "status": 200})
    except Exception as e:
        return jsonify({"database": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 0.0.0.0 est nécessaire pour écouter sur toutes les interfaces du conteneur
    app.run(host='0.0.0.0', port=5000)

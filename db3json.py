from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
from flask_login import UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ziyaret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def export_user_to_json():
    with app.app_context():

        db.create_all()
        users = User.query.all()

        data = []
        for user in users:
            data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password
            })

        json_path = os.path.join(os.path.dirname(__file__), 'users.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} kullanıcı başarıyla {json_path} dosyasına kaydedildi.")

if __name__ == '__main__':
    export_user_to_json()

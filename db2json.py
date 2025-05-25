from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ziyaret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ziyaretci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    tc = db.Column(db.String(11))
    telefon = db.Column(db.String(20), nullable=False)
    tarih = db.Column(db.String(20), nullable=False)
    sure = db.Column(db.Integer, nullable=False)
    ziyaret_sebebi = db.Column(db.String(50), nullable=False)
    ziyaret_edilen = db.Column(db.String(100), nullable=False)
    notlar = db.Column(db.Text)

def export_ziyaretci_to_json():
    with app.app_context():
  
        db.create_all()
        ziyaretciler = Ziyaretci.query.all()

        data = []
        for ziyaretci in ziyaretciler:
            data.append({
                "id": ziyaretci.id,
                "ad": ziyaretci.ad,
                "soyad": ziyaretci.soyad,
                "tc": ziyaretci.tc,
                "telefon": ziyaretci.telefon,
                "tarih": ziyaretci.tarih,
                "sure": ziyaretci.sure,
                "ziyaret_sebebi": ziyaretci.ziyaret_sebebi,
                "ziyaret_edilen": ziyaretci.ziyaret_edilen,
                "notlar": ziyaretci.notlar
            })

        json_path = os.path.join(os.path.dirname(__file__), 'ziyaretciler.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} ziyaretçi başarıyla {json_path} dosyasına kaydedildi.")

if __name__ == '__main__':
    export_ziyaretci_to_json()



- **Ziyaretçi Giriş/Çıkış Kaydı:** Gelen ve ayrılan kişilerin kaydını tutar.  
- **Randevu Yönetimi:** Ziyaretçiler için önceden randevu oluşturulabilir.  
- **Kullanıcı Yönetimi:** Kullanıcı rolleri ve oturum yönetimi sağlar.  
- **Raporlama & Filtreleme:** Ziyaretçi bilgileri tarih veya kullanıcı bazlı filtrelenebilir.  
- **JSON Desteği:** Ziyaretçi ve kullanıcı verileri JSON formatında dışa aktarılabilir.  
- **Veritabanı:** SQLite kullanılarak kalıcı veri saklama sağlanır.



```
ziyaretci-dosyasi-yeni/
│
├── app.py                   # Ana Flask uygulaması
├── db2json.py, db3json.py   # Veritabanını JSON'a dönüştüren araçlar
├── instance/ziyaret.db      # SQLite veritabanı
├── templates/               # HTML şablonlar (Jinja2)
│   ├── anasayfa.html
│   ├── giris.html
│   ├── kayit.html
│   ├── randevu.html
│   └── ...
├── static/                  # CSS, JS, görseller (eğer varsa)
├── users.json               # Kullanıcı verileri
├── ziyaretciler.json        # Ziyaretçi verileri
├── requirements.txt         # Gerekli Python paketleri
└── README.md                # Proje açıklama dosyası
```




```bash
git clone https://github.com/kullaniciadi/ziyaretci-sistemi.git
cd ziyaretci-sistemi
```


```bash
python -m venv venv
source venv/bin/activate  
```


```bash
pip install -r requirements.txt
```


```bash
python app.py
```


```
http://127.0.0.1:5000/
```



- Python 3.7+
- Flask
- Jinja2
- Werkzeug
- (Diğer bağımlılıklar `requirements.txt` dosyasında listelenmiştir.)



1. Fork oluşturun.
2. Yeni bir dal (branch) açın: `git checkout -b yeni-ozellik`
3. Değişikliklerinizi yapın ve commitleyin.
4. Pull Request (PR) gönderin.



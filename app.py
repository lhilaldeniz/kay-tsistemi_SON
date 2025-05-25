from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from datetime import datetime 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ziyaret.db' 
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'giris'
@login_manager.unauthorized_handler
def yetkisiz_erisim():
    flash("Oturumunuz sona erdi veya yetkiniz yok. Lütfen tekrar giriş yapın.", "warning")
    return redirect(url_for("giris"))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

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

class Randevu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    neden = db.Column(db.String(100), nullable=False)
    hedef_kisi = db.Column(db.String(100), nullable=False)
    tarih = db.Column(db.String(20), nullable=False)
    saat = db.Column(db.String(10), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def ana_sayfa():
    return render_template("anasayfa.html")

@app.route("/kayit", methods=["GET", "POST"])
@login_required
def kayit():
    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        tc = request.form.get("tc")
        telefon = request.form.get("telefon")
        tarih = request.form.get("tarih")
        sure = request.form.get("sure")
        ziyaret_sebebi = request.form.get("ziyaret_sebebi")
        ziyaret_edilen = request.form.get("ziyaret_edilen")
        notlar = request.form.get("notlar")

        yeni_ziyaretci = Ziyaretci(
            ad=ad,
            soyad=soyad,
            tc=tc,
            telefon=telefon,
            tarih=tarih,
            sure=sure,
            ziyaret_sebebi=ziyaret_sebebi,
            ziyaret_edilen=ziyaret_edilen,
            notlar=notlar
        )

        db.session.add(yeni_ziyaretci)
        db.session.commit()

        flash(f"{ad} {soyad} adlı ziyaretçi başarıyla kaydedildi.", "success")
        return redirect(url_for("liste"))

    return render_template("kayit.html")

@app.route("/giris", methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        kullanici = User.query.filter_by(email=email).first()

        if not kullanici:
            flash("E-posta adresi bulunamadı", "danger")
        elif bcrypt.check_password_hash(kullanici.password, password):
            login_user(kullanici)
            flash("Giriş başarılı!", "success")
            return redirect(url_for("panel_giris"))
        else:
            flash("Hatalı şifre", "danger")

    return render_template("giris.html")

@app.route("/cikis")
@login_required
def cikis():
    logout_user()
    flash("Çıkış yapıldı", "info")
    return redirect(url_for("giris"))

@app.route("/liste")
@login_required
def liste():
    ziyaretciler = Ziyaretci.query.all()
    return render_template("liste.html", ziyaretciler=ziyaretciler)

@app.route("/filtre", methods=["GET", "POST"])
@login_required
def filtre():
    filtrelenmis_ziyaretciler = []

    if request.method == "POST":
        ad_soyad = request.form.get("ad_soyad")
        telefon = request.form.get("telefon")
        sebep = request.form.get("sebep")
        baslangic_tarih = request.form.get("baslangic_tarih")
        bitis_tarih = request.form.get("bitis_tarih")

        query = Ziyaretci.query

        if ad_soyad:
            query = query.filter(
                (Ziyaretci.ad.ilike(f"%{ad_soyad}%")) | 
                (Ziyaretci.soyad.ilike(f"%{ad_soyad}%"))
            )

        if telefon:
            query = query.filter(Ziyaretci.telefon.ilike(f"%{telefon}%"))

        if sebep:
            query = query.filter(Ziyaretci.ziyaret_sebebi == sebep)

        if baslangic_tarih:
            query = query.filter(Ziyaretci.tarih >= baslangic_tarih)

        if bitis_tarih:
            query = query.filter(Ziyaretci.tarih <= bitis_tarih)

        filtrelenmis_ziyaretciler = query.all()

    return render_template("filtre.html", filtrelenmis_ziyaretciler=filtrelenmis_ziyaretciler)

@app.route("/rapor")
@login_required
def rapor():
    ziyaretciler = Ziyaretci.query.all()
    toplam_ziyaretci = Ziyaretci.query.count()

    bugunku_ziyaretci = Ziyaretci.query.filter_by(tarih=datetime.now().strftime("%Y-%m-%d")).count()

    en_yogun_sebep = db.session.query(
        Ziyaretci.ziyaret_sebebi, db.func.count(Ziyaretci.ziyaret_sebebi)
    ).group_by(Ziyaretci.ziyaret_sebebi).order_by(db.func.count(Ziyaretci.ziyaret_sebebi).desc()).first()

    if en_yogun_sebep:
        en_yogun_sebep = en_yogun_sebep[0]
    else:
        en_yogun_sebep = "Veri yok"

    return render_template("rapor.html",
                           ziyaretciler=ziyaretciler,
                           toplam_ziyaretci=toplam_ziyaretci,
                           bugunku_ziyaretci=bugunku_ziyaretci,
                           en_yogun_sebep=en_yogun_sebep)

@app.route("/panel_giris")
@login_required
def panel_giris():
    total_visitors = Ziyaretci.query.count()
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_visitors = Ziyaretci.query.filter(Ziyaretci.tarih == today_date).count()
    total_users = User.query.count()

    return render_template(
        "panel_giris.html",
        total_visitors=total_visitors,
        today_visitors=today_visitors,
        total_users=total_users
    )

@app.route("/kullanici_kayit", methods=["GET", "POST"])
def kullanici_kayit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        yeni_kullanici = User(name=name, email=email, password=hashed_password)

        db.session.add(yeni_kullanici)
        db.session.commit()

        flash("Kullanıcı kaydı başarılı!", "success")
        return redirect(url_for("giris"))

    return render_template("kullanici_kayit.html")

@app.route("/randevu", methods=["GET", "POST"])
def randevu():
    if request.method == "POST":
        ad_soyad = request.form.get("ad_soyad")
        telefon = request.form.get("telefon")
        neden = request.form.get("neden")
        hedef_kisi = request.form.get("hedef_kisi")
        tarih = request.form.get("tarih")
        saat = request.form.get("saat")

        yeni_randevu = Randevu(
            ad_soyad=ad_soyad,
            telefon=telefon,
            neden=neden,
            hedef_kisi=hedef_kisi,
            tarih=tarih,
            saat=saat
        )
        db.session.add(yeni_randevu)
        db.session.commit()

        flash("Randevunuz başarıyla alındı.", "success")
        return redirect(url_for("panel_giris"))

    return render_template("randevu.html")




@app.route("/randevu_liste")
@login_required
def randevu_liste():
    randevular = Randevu.query.all()
    return render_template("randevu_liste.html", randevular=randevular)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

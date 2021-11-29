from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.sql.schema import ForeignKey
from flask_sqlalchemy  import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:bahadir@localhost/testing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisisthesecretkey' #BUNU DA ARASTIR

db=SQLAlchemy(app)



class Tarif(db.Model):
    __tablename__ = 'Tarifler'
    tarif_id = db.Column(db.Integer(), primary_key = True)
    tarif_adi = db.Column(db.String())
    yemek_tarifi = db.Column(db.String())
    olusturulma_tarihi = db.Column(db.Date())
    #kullanici_adi = db.Column(db.String(), ForeignKey = 'Kullanicilar.kullanici_adi')

    def __init__(self,tarif_id,tarif_adi,yemek_tarifi,olusturulma_tarihi,kullanici_adi):
        self.tarif_id = tarif_id
        self.tarif_adi=tarif_adi
        self.yemek_tarifi = yemek_tarifi
        self.olusturulma_tarihi=olusturulma_tarihi 
        self.kullanici_adi = kullanici_adi



class Besin(db.Model):
    __tablename__ = 'Besinler'
    besin_adi = db.Column(db.String(),primary_key = True)
    karbonhidrat_degeri = db.Column(db.Float())
    protein_degeri = db.Column(db.Float())
    yag_degeri = db.Column(db.Float())
    kalori = db.Column(db.Integer())
    def __init__(self, besin_adi, karbonhidrat_degeri, protein_degeri,yag_degeri, kalori):
        self.besin_adi = besin_adi
        self.karbonhidrat_degeri = karbonhidrat_degeri
        self.protein_degeri = protein_degeri
        self.yag_degeri = yag_degeri
        self.kalori = kalori



# Safa Demirhan
class Egzersizler(db.Model):
    __tablename__ = 'Egzersizler'
    e_id = db.Column(db.Integer(), primary_key=True)
    egzersiz_adi = db.Column(db.String())
    yakilan_kalori = db.Column(db.Integer())
    def __init__(self, e_id, egzersiz_adi, yakilan_kalori):
        self.e_id = e_id
        self.egzersiz_adi = egzersiz_adi
        self.yakilan_kalori = yakilan_kalori



# Safa Demirhan
class HazirDiyetler(db.Model):
    __tablename__ = 'HazirDiyetler'
    diyet_adi = db.Column(db.String(), primary_key=True)
    diyet_icerigi = db.Column(db.String())
    diyet_kalori = db.Column(db.Float())
    def __init__(self, diyet_adi, diyet_icerigi, diyet_kalori):
        self.diyet_adi = diyet_adi
        self.diyet_icerigi = diyet_icerigi
        self.diyet_kalori = diyet_kalori



# Safa Demirhan
class Gonderiler(db.Model):
    __tablename__ = 'Gonderiler'
    gonderi_adi = db.Column(db.Integer(), primary_key=True)
    kullanici_adi = db.Column(db.String())
    # Image type kullan
    resim = db.Column(db.String)
    resim_aciklamasi = db.Column(db.String())
    olusturulma_tarihi = db.Column(db.Date())
    def __init__(self, gonderi_adi, kullanici_adi, resim, resim_aciklamasi, olusturulma_tarihi):
        self.gonderi_adi = gonderi_adi
        self.kullanici_adi = kullanici_adi
        self.resim = resim
        self.resim_aciklamasi = resim_aciklamasi
        self.olusturulma_tarihi = olusturulma_tarihi

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tarifler')
def tarifler():
    tarifler = Tarif.query.all()
    return render_template('tarifler.html', tarifler = tarifler)

# @app.route('/tarif/sil')
# def tarifsil():


@app.route('/besinler')
def besinler():
    besinler = Besin.query.all()
    return render_template('besinler.html',besinler = besinler)

# Safa Demirhan
@app.route('/hazir_diyetler')
def hazir_diyetler():
    hazir_diyetler = HazirDiyetler.query.all()
    return render_template('hazir_diyetler.html',hazir_diyetler = hazir_diyetler)

# Safa Demirhan
@app.route('/egzersizler')
def egzersizler():
    e_id = Egzersizler.query.all()
    return render_template('egzersizler.html',e_id = e_id)

# Safa Demirhan
@app.route('/gonderiler')
def gonderiler():
    gonderi_adi = Gonderiler.query.all()
    return render_template('gonderiler.html',gonderi_adi = gonderi_adi)

@app.route('/besinekle', methods = ['POST'])
def besinekle():
    if request.method == 'POST':
        yeni_besin = Besin (besin_adi= request.form['besin_adi'], karbonhidrat_degeri= request.form['karbonhidrat_degeri'], protein_degeri= request.form['protein_degeri'], yag_degeri= request.form['yag_degeri'], kalori=request.form['kalori']) 
        db.session.add(yeni_besin)
        db.session.commit()
        return redirect(url_for('besinler'))

@app.route('/tarifekle', methods=['POST'])
def tarifekle():
    if request.method == 'POST':
        test = "bahadir"
        yeni_tarif = Tarif(tarif_id=request.form['tarif_id'], tarif_adi= request.form['tarif_adi'], yemek_tarifi= request.form['yemek_tarifi'],olusturulma_tarihi= request.form['olusturulma_tarihi'],kullanici_adi=test)#request.form['kullanici_adi'])
        db.session.add(yeni_tarif)
        db.session.commit()
        return (redirect(url_for('tarifler')))

# Safa Demirhan
@app.route('/hazirdiyetekle', methods = ['POST'])
def hazirdiyetekle():
    if request.method == 'POST':
        yeni_hazir_diyet = HazirDiyetler(diyet_adi= request.form['diyet_adi'], diyet_icerigi= request.form['diyet_icerigi'], diyet_kalori= request.form['diyet_kalori']) 
        db.session.add(yeni_hazir_diyet)
        db.session.commit()
        flash('Hazır diyet eklenmiştir!', 'success')
        return redirect(url_for('hazir_diyetler'))

# Safa Demirhan
@app.route('/egzersizekle', methods = ['POST'])
def egzersizekle():
    if request.method == 'POST':
        yeni_egzersiz = Egzersizler(e_id= request.form['e_id'], egzersiz_adi= request.form['egzersiz_adi'], yakilan_kalori= request.form['yakilan_kalori']) 
        db.session.add(yeni_egzersiz)
        db.session.commit()
        flash('Egzersiz eklenmiştir!', 'success')
        return redirect(url_for('egzersizler'))

@app.route('/tarifsil', methods= ['POST'])
def tarifsil():
    tarif_id = request.form['tarif_id']
    silinecek_tarif = Tarif.query.filter_by(tarif_id = tarif_id).first()
    db.session.delete(silinecek_tarif)
    db.session.commit()    
    return redirect(url_for('tarifler'))

@app.route('/besinsil', methods = ['POST'])
def besinsil():
    besin_adi = request.form['besin_adi']
    silinecek_besin = Besin.query.filter_by(besin_adi = besin_adi).first()
    db.session.delete(silinecek_besin)
    db.session.commit()
    return redirect(url_for('besinler'))    

# Safa Demirhan
@app.route('/hazirdiyetsil', methods = ['POST'])
def hazirdiyetsil():
    diyet_adi = request.form['diyet_adi']
    silinecek_tarif = HazirDiyetler.query.filter_by(diyet_adi = diyet_adi).first()
    db.session.delete(silinecek_tarif)
    db.session.commit()
    flash('Hazır diyet silinmiştir!', 'success')
    return redirect(url_for('hazir_diyetler'))

# Safa Demirhan
@app.route('/egzersizsil', methods = ['POST'])
def egzersizsil():
    e_id = request.form['e_id']
    silinecek_egzersiz = Egzersizler.query.filter_by(e_id = e_id).first()
    db.session.delete(silinecek_egzersiz)
    db.session.commit()
    flash('Egzersiz silinmiştir!', 'success')
    return redirect(url_for('egzersizler'))

@app.route('/besinduzenle', methods = ['POST'])
def besinduzenle():
    #besin = Besin.query.filter_by(besin_adi = request.form['besin_adi'])
    besin_adi =request.form['besin_adi']
    return render_template('besinduzenle.html',besin_adi = besin_adi)

@app.route('/besinduzenle2', methods=['POST'])
def besinduzenle2():
    besin_adi = request.form['besin_adi']
    duzenlenecek_besin = Besin.query.filter_by(besin_adi=besin_adi).first()

    yeni_ad = request.form['besin_adi']
    yeni_karbonhidrat = request.form['karbonhidrat_degeri']
    yeni_protein = request.form['protein_degeri']
    yeni_yag = request.form['yag_degeri']
    yeni_kalori = request.form['kalori']

    if yeni_ad == '':
        yeni_ad = duzenlenecek_besin.besin_adi
    if yeni_karbonhidrat == '':
        yeni_karbonhidrat = duzenlenecek_besin.karbonhidrat_degeri
    if yeni_protein == '':
        yeni_protein = duzenlenecek_besin.protein_degeri
    if yeni_yag == '':
        yeni_yag = duzenlenecek_besin.yag_degeri
    if yeni_kalori == '':
        yeni_kalori=duzenlenecek_besin.kalori

    duzenlenecek_besin.besin_adi = yeni_ad
    duzenlenecek_besin.karbonhidrat_degeri = yeni_karbonhidrat
    duzenlenecek_besin.protein_degeri = yeni_protein
    duzenlenecek_besin.yag_degeri = yeni_yag
    duzenlenecek_besin.kalori = yeni_kalori

    db.session.commit()

    return redirect(url_for('besinler')) 

# Safa Demirhan
@app.route('/hazirdiyetduzenle', methods = ['POST'])
def hazirdiyetduzenle():
    #besin = Besin.query.filter_by(diyet_adi = request.form['diyet_adi'])
    diyet_adi =request.form['diyet_adi']
    return render_template('hazirdiyetduzenle.html',diyet_adi = diyet_adi)

@app.route('/hazirdiyetduzenle2', methods=['POST'])
def hazirdiyetduzenle2():
    diyet_adi = request.form['diyet_adi']
    duzenlenecek_hazirdiyet = Besin.query.filter_by(diyet_adi=diyet_adi).first()

    yeni_diyet_adi = request.form['diyet_adi']
    yeni_diyet_icerigi = request.form['diyet_icerigi']
    yeni_diyet_kalori = request.form['diyet_kalori']

    if yeni_diyet_adi == '':
        yeni_diyet_adi = duzenlenecek_hazirdiyet.diyet_adi
    if yeni_diyet_icerigi == '':
        yeni_diyet_icerigi = duzenlenecek_hazirdiyet.diyet_icerigi
    if yeni_diyet_kalori == '':
        yeni_diyet_kalori = duzenlenecek_hazirdiyet.diyet_kalori

    duzenlenecek_hazirdiyet.diyet_adi = yeni_diyet_adi
    duzenlenecek_hazirdiyet.diyet_icerigi = yeni_diyet_icerigi
    duzenlenecek_hazirdiyet.diyet_kalori = yeni_diyet_kalori
    db.session.commit()
    return redirect(url_for('hazir_diyetler')) 

# Safa Demirhan
@app.route('/egzersizduzenle', methods = ['POST'])
def egzersizduzenle():
    #besin = Besin.query.filter_by(e_id = request.form['e_id'])
    e_id =request.form['e_id']
    return render_template('besinduzenle.html',e_id = e_id)

@app.route('/egzersizduzenle2', methods=['POST'])
def egzersizduzenle2():
    e_id = request.form['e_id']
    duzenlenecek_egzersiz = Besin.query.filter_by(e_id=e_id).first()

    yeni_id = request.form['e_id']
    yeni_ad = request.form['egzersiz_adi']
    yeni_kalori = request.form['yakilan_kalori']

    if yeni_id == '':
        yeni_id = duzenlenecek_egzersiz.e_id
    if yeni_ad == '':
        yeni_ad = duzenlenecek_egzersiz.egzersiz_adi
    if yeni_kalori == '':
        yeni_kalori = duzenlenecek_egzersiz.yakilan_kalori

    duzenlenecek_egzersiz.e_id = yeni_id
    duzenlenecek_egzersiz.egzersiz_adi = yeni_ad
    duzenlenecek_egzersiz.yakilan_kalori = yeni_kalori
    db.session.commit()
    return redirect(url_for('besinler'))

if __name__ == '__main__':   
    app.run(debug = True)

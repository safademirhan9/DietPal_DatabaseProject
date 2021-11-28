from flask import Flask, render_template, redirect, url_for, request
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
    #
    # Has Relationship with GunlukAktivite, named "Olusur: e_id, aktivite_id"
    #
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

if __name__ == '__main__':   
    app.run(debug = True)

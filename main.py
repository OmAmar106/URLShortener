from flask import Flask,render_template, redirect ,request
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///shorturls.sqlite"
db = SQLAlchemy(app)

class URL(db.Model):
    __tablename__ = 'URL'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    OrignalURL = db.Column(db.String)
    NewURL = db.Column(db.String,unique=True)

def randomgenerate():
    L = [1,2,3,4,5,6,7,8,9,0,'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    st = ''
    for i in range(7):
        randomno = random.randint(0,35)
        st += str(L[randomno])
    r = URL.query.filter_by(NewURL=st).first()
    if r:
        return randomgenerate()
    return st

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        Givenurl = request.form.get('orignal')
        c = randomgenerate()
        d = URL(OrignalURL=Givenurl,NewURL=c)
        db.session.add(d)
        db.session.commit()
        curpath = request.url_root+request.path
        c = curpath+c
        return render_template('index.html',orignal=Givenurl,new=c)
    else:
        return render_template('index.html',orignal='',new='')
    
@app.route('/<string:s>')
def newpage(s):
    r = URL.query.filter_by(NewURL=s).first()
    if r:
        return redirect(r.OrignalURL)
    else:
        return "URL not in database"

if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

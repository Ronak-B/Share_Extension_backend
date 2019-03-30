from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.config['SECRET_KEY']='5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///extension.db'

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String)
    name=db.Column(db.String)
    email=db.Column(db.String)
    password=db.Column(db.String)

class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    sender=db.Column(db.String)
    receiver=db.Column(db.String)
    message=db.Column(db.String(200))

@app.route("/signup",methods=["POST"])
def signup():
    password=generate_password_hash(request.form['password'],method='sha256')
    new_user=User(username=request.form['username'],name=request.form['name'],email=request.form['email'],password=password)
    print(request.form['username']+request.form['name']+request.form['email']+password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'result':'success'})

@app.route('/login',methods=['POST'])
def login():
    user=User.query.filter_by(username=request.form['username']).first()
    if user:
        if check_password_hash(user.password,request.form['password']):
            return jsonify({'result':'success'})
        else :
            return jsonify({'result':'failed'})
    else :
        return jsonify({'result':'failed'})
if __name__ == "__main__":
    app.run(debug=True)
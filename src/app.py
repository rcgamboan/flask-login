
from flask import Flask, flash, redirect, render_template, request, url_for, flash
from config import config
import sqlite3 as sql

#Models
from models.ModelUser import ModelUser

#Entities
from models.entities.User import User

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = User(0,request.form['username'],request.form['password'])
        user.username = user.username[0]
        db = sql.connect("./src/database.db")
        logged_user , isAdmin = ModelUser.login(db,user)
        # print(isAdmin)
        if logged_user != None:
            if logged_user.password:

                if isAdmin == 0:
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('admin'))
            else:
                flash("Alguno de los datos es incorrecto. ")
                return render_template('auth/login.html')    
        else:
            flash("Alguno de los datos es incorrecto. ")
            return render_template('auth/login.html')    
    else:
        return render_template('auth/login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()


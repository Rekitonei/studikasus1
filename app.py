from cs50 import SQL
import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)
db = SQL("sqlite:///score.db")
udb = SQL("sqlite:///user.db")
app.config.update(SECRET_KEY=os.urandom(24))
@app.route("/", methods=["GET", "POST"])
def index():
        if request.method == "POST": 
            name = request.form.get("name")
            score = request.form.get("score")

            db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name, score)

            return redirect("/")
        else:

            students = db.execute("SELECT * FROM score")
            return render_template("index.html", students=students)
            
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "GET":
        score = db.execute("SELECT * FROM score WHERE id = ?", id)[0]
        print(score)
        return render_template("edit.html", score=score)
    elif request.method == "POST":
        score_name = request.form.get("name")
        score_score = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_score, id)
        return redirect("/") 
@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db.execute("delete from score where id = ?", id)
    return redirect("/") 

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("Username"):
            return "must provide username"
        elif not request.form.get("Passwrod"):
            return "must provide password"
        rows = udb.execute("SELECT * FROM user WHERE Username = ?", request.form.get("Username"))

        email = request.form.get("Email")
        name_user = request.form.get("Name")
        username = request.form.get("Username")
        password = request.form.get("Password")
        password_repeat = request.get("rpassword")

        print(email)
        print(name_user)
        print(username)
        print(password)

        hash = generate_password_hash(password)
        if len(rows) == 1:
            return "username already taken"
        if password == password_repeat:
            udb.execute("INSERT INTO user (username, hash) VALUES(?, ?)", username, hash)

            registered_user = udb.execute("select * from user where username = ?", username)
            session["id"] = registered_user[0]["id"]
            flash("you were sucessfully registered")
            return redirect("/")

        else:

            return render_template("register.html", userdb=userdb)
        
    else:
        return render_template("register.html")
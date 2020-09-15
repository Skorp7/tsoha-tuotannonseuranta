from app import app
from flask import render_template, request, redirect
import users, visits
from db import db
from flask import session

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)


@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut, kokeile toista käyttäjätunnusta.")

@app.route("/admin", methods=["get"])
def admin():
    if request.method == "GET":
        if users.user_status() == 1:
            return render_template("admin.html")
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
        
@app.route("/change_status", methods=["get","post"])
def change_status():
    if request.method == "GET":
        user_list = users.user_list()
        return render_template("change_status.html", user_list=user_list)
    if request.method == "POST":
        new_status = request.form["new_status"]
        username = request.form["username"]
        if users.update_status(username, new_status):
            return redirect("/")
        else:
            return render_template("error.html",message="Statuksen vaihto epäonnistui.")

@app.route("/production")
def production():
    return render_template("production.html")

from app import app
from flask import render_template, request, redirect
import users, visits, os, orders, customers, datetime, events
from datetime import date
from db import db
from flask import session

@app.route("/")
def index():
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
            session["csrf_token"] = os.urandom(16).hex()
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/charts")
def charts():
    if users.user_status() == 1:
        return render_template("charts.html")
    else:
        return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    

@app.route("/new_event", methods=["get","post"])
def new_event():
    user_data = users.user()
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_event.html", user_data = user_data)
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        order_id = request.form["order_id"]
        description = request.form["description"]
        user_id = user_data[0]
        is_pending = request.form["is_pending"]
        token = request.form["csrf_token"]
        print('tilausid: ' + str(orders.order(order_id)))
        print('ispendind: ' + str(is_pending) + ' user_id: ' + str(user_id) + ' description: ' + description)
        if orders.order(order_id) != None and description != '' and events.add(order_id, user_id, description, is_pending) and session["csrf_token"] == token:
            return redirect("/production")
        else:
            return render_template("error.html",message="Työvaiheen lisääminen ei onnistunut.")

@app.route("/seek")
def seek():
    if users.user_status() == 1 or users.user_status() == 0:
        return render_template("seek.html")
    else:
        return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")

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
        if users.user_status() == 1:
            user_list = users.user_list()
            return render_template("change_status.html", user_list=user_list)
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        new_status = request.form["new_status"]
        username = request.form["username"]
        token = request.form["csrf_token"]
        if users.update_status(username, new_status) and session["csrf_token"] == token:
            return redirect("/admin")
        else:
            return render_template("error.html",message="Statuksen vaihto epäonnistui.")


@app.route("/new_order", methods=["get","post"])
def new_order():
    order_type_list = orders.order_type_list()
    customer_list = customers.customer_list()
    clinic_list = customers.clinic_list()
    message = ''
       
    if request.method == "POST" :
        clinic_id = request.form["clinic_id"]
        order_type_id = request.form["order_type_id"]
        customer_id = request.form["customer_id"]
        d_date = request.form["delivery_date"]
        d_time = request.form["delivery_time"]
        delivery_date = d_date + ' ' + d_time + ':00.000000'
        token = request.form["csrf_token"]
        if clinic_id == '0' or order_type_id == '0' or customer_id == '0' or d_date == '':
            message = "Täytä kaikki kentät!"
        elif clinic_id != '0' or order_type_id != '0' or customer_id != '0' and session["csrf_token"] == token:
            latest_id = orders.add(order_type_id, customer_id, delivery_date, clinic_id)
            if (latest_id != None):
                message = 'Tilaus lisätty! Uuden tilauksen id on: ' + str(latest_id) + ' Kirjoita se lähetteeseen.'
        else:
           return render_template("error.html",message="Tilauksen lisäys epäonnistui.")

    if users.user_status() == 1 or users.user_status() == 0:
        return render_template('new_order.html', message=message, order_type_list=order_type_list, customer_list=customer_list, clinic_list=clinic_list)
    else:
        return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    


@app.route("/new_order_type", methods=["get","post"])
def new_order_type():
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_order_type.html")
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        product = request.form["product"]
        materials = request.form["materials"]
        token = request.form["csrf_token"]
        if orders.add_order_type(product, materials) and session["csrf_token"] == token:
            return redirect("/new_order")
        else:
            return render_template("error.html",message="Tuotteen lisääminen ei onnistunut.")

@app.route("/new_clinic", methods=["get","post"])
def new_clinic():
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            citys = customers.citys_fi()
            return render_template("new_clinic.html", citys=citys)
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        name = request.form["name"]
        adress = request.form["adress"]
        city = request.form["city"]
        postal = request.form["postal"]
        token = request.form["csrf_token"]
        if customers.add_clinic(name, adress, postal, city) and session["csrf_token"] == token:
            return redirect("/new_order")
        else:
            return render_template("error.html",message="Toimipisteen lisääminen ei onnistunut. Tarkista onko sama toimipiste jo olemassa samassa kaupungissa ja täytä kaikki kentät.")

@app.route("/new_customer", methods=["get","post"])
def new_customer():
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_customer.html")
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        name = request.form["name"]
        token = request.form["csrf_token"]
        if customers.add(name) and session["csrf_token"] == token:
            return redirect("/new_order")
        else:
            return render_template("error.html",message="Asiakkaan lisääminen epäonnistui.")


date = date.today()

@app.route("/production", methods=["get"])
def production():
    order_list = orders.list(date.strftime("%Y-%m-%d"))
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("production.html", date=date, order_list=order_list)
        else:
            return render_template("error.html",message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")

@app.errorhandler(404)
def error(e):
    return render_template("error.html")

@app.errorhandler(500)
def server_error(e):
    return redirect("/")

@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
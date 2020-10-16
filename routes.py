from app import app
from flask import render_template, request, redirect, flash
import users
import os
import orders
import customers
import datetime
import events
from datetime import date
from db import db
from flask import session


@app.route("/", methods=["GET", "POST"])
def index():
    time = datetime.datetime.now()
    date = time.strftime("%d.%m.%Y")
    if request.method == "GET":
        return render_template("index.html", time=time.strftime("%H:%M"), date=date)
    if request.method == "POST":
        token = request.form["csrf_token"]
        session["show_tips"] = request.form["show_tips"]
        if session["csrf_token"] == token:
            return render_template("index.html", time=time.strftime("%H:%M"), date=date)
        else:
            return render_template("error.html", message="")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["csrf_token"] = os.urandom(16).hex()
            session["show_tips"] = "1"
            return redirect("/")
        else:
            flash("Väärä tunnus tai salasana", "warning")
            return redirect(request.url)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/charts")
def charts():
    amount_order_list = [list(elem) for elem in orders.amount_orders_list()]
    hard_worker_list = events.hard_workers()
    queue_durations = events.queue_durations()
    user_counter = len(users.user_list())
    fav_customers = orders.fav_customers()
    if users.user_status() == 1:
        return render_template("charts.html", user_counter=user_counter, hard_worker_list=hard_worker_list,
                               queue_durations=queue_durations, amount_order_list=amount_order_list,
                               fav_customers=fav_customers)
    else:
        return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")


@app.route("/new_event", methods=["GET", "POST"])
def new_event():
    user_data = users.user()
    order_list = orders.listAll()
    order_list_not_tuple = [list(elem) for elem in order_list]
    event_list = [list(elem) for elem in events.event_list()]
    event_descr_list = events.common_events()
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_event.html", user_data=user_data, order_list=order_list,
                                   order_list_not_tuple=order_list_not_tuple,
                                   event_list=event_list, event_descr_list=event_descr_list)
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        order_id = request.form["order_id"]
        description_drop = request.form["description_drop"]
        description_text = request.form["description_text"]
        description = ""
        if (description_drop != ""):
            description = description_drop
        elif (description_text != ""):
            description = description_text
        else:
            flash("Valitse työvaiheen kuvaus listasta tai kirjoita kuvaus", "warning")
            return redirect(request.url)
        user_id = user_data[0]
        is_pending = request.form["is_pending"]
        in_progress = request.form["in_progress"]
        token = request.form["csrf_token"]
        if orders.seek(order_id) != None and description != "" and \
            events.add(order_id, user_id, description, is_pending) and session["csrf_token"] == token:
            if in_progress == "0":
                orders.check_out_in(order_id, in_progress)
                events.add(order_id, user_id, "Uloskirjaus", 0)
            flash("Työvaihe '" + description +
                  "' lisätty tilaukselle " + order_id, "success")
            return redirect(request.url)
        else:
            flash("Työvaiheen lisääminen epäonnistui", "warning")
            return redirect(request.url)


@app.route("/seek_by_user")
def seek_by_user():
    event_list = events.event_list()
    username = users.user()[1]
    user_id = users.user()[0]
    if users.user_status() == 1 or users.user_status() == 0:
        return render_template("seek_by_user.html", event_list=event_list, user_id=user_id, username=username)
    else:
        return render_template("error.html", message="Haku ei onnistunut")


@app.route("/seek/")
def seek():
    order_list = orders.listAll()
    event_list = events.event_list()
    order_id = request.args.get("order_id", "")
    search_word = request.args.get("search", "")
    search_data = orders.seekAll(search_word)
    now = datetime.datetime.now()
    # seek all orders is allowed only for admins
    if (len(search_word) < 3):
        search_data = None
    if users.user_status() == 1 or users.user_status() == 0:
        return render_template("seek.html", event_list=event_list, order_list=order_list, order_id=order_id, 
        search_data=search_data, now=now)
    else:
        return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if users.seek(username):
            flash("Käyttäjänimi on varattu", "warning")
        if password != password2:
            flash("Salasanat eivät täsmää", "warning")
        if password != password2 or users.seek(username):
            return redirect(request.url)
        if users.register(username, password):
            flash("Käyttäjätunnus '" + username + "' luotu", "success")
            return redirect("/")
        else:
            flash("Rekisteröinti epäonnistui. Käyttäjätunnus '" +
                  username + "' on ehkä jo olemassa", "warning")
            return redirect(request.url)


@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        if users.user_status() == 1:
            user_list = users.user_list()
            now = datetime.datetime.now()
            search_data = orders.seekAll(request.args.get("search", None))
            return render_template("admin.html", user_list=user_list, search_data=search_data, now=now)
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        user_id = request.form["user_id"]
        username = users.userById(user_id)[1]
        event_list = events.event_list()
        token = request.form["csrf_token"]
        if session["csrf_token"] == token:
            return render_template("seek_by_user.html", event_list=event_list, user_id=user_id, username=username)
        else:
            return render_template("error.html", message="Haku ei onnistunut")


@app.route("/change_status", methods=["GET", "POST"])
def change_status():
    if request.method == "GET":
        if users.user_status() == 1:
            user_list = users.user_list()
            return render_template("change_status.html", user_list=user_list)
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        new_status = request.form["new_status"]
        user_id = request.form["user_id"]
        token = request.form["csrf_token"]
        if users.update_status(user_id, new_status) and session["csrf_token"] == token:
            flash("Käyttäjän '" + users.userById(user_id)[1] + "' oikeudet päivitetty", "success")
            return redirect(request.url)
        else:
            flash("Oikeuksien päivitys epäonnistui", "warning")
            return redirect(request.url)


@app.route("/new_order", methods=["GET", "POST"])
def new_order():
    today_datetime = datetime.datetime.now()
    order_type_list = orders.order_type_list()
    customer_list = customers.customer_list()
    clinic_list = customers.clinic_list()
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_order.html", order_type_list=order_type_list, customer_list=customer_list,
                                   clinic_list=clinic_list)
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        clinic_id = request.form["clinic_id"]
        order_type_id = request.form["order_type_id"]
        customer_id = request.form["customer_id"]
        d_date = request.form["delivery_date"]
        d_time = request.form["delivery_time"]
        delivery_date = d_date + " " + d_time + ":00.000000"
        dd_datetime = datetime.datetime.strptime(
            delivery_date, "%Y-%m-%d %H:%M:%S.%f")
        token = request.form["csrf_token"]
        if clinic_id == "0" or order_type_id == "0" or customer_id == "0" or d_date == "":
            flash("Täytä kaikki kentät!", "warning")
            return redirect(request.url)
        if dd_datetime - today_datetime < datetime.timedelta(minutes=1):
            flash("Pyydetty toimitusaika on menneisyydessä", "warning")
            return redirect(request.url)
        elif clinic_id != "0" or order_type_id != "0" or customer_id != "0" and session["csrf_token"] == token:
            latest_id = orders.add(
                order_type_id, customer_id, delivery_date, clinic_id)
            if (latest_id != None):
                events.add(latest_id, users.user()[0], "Sisäänkirjaus", 0)
                flash("Tilaus lisätty! Tilauksen id on: " +
                      str(latest_id) + ". Kirjoita se lähetteeseen.", "success")
                return redirect(request.url)
        else:
            flash("Tilauksen lisääminen epäonnistui", "warning")
            return redirect(request.url)


@app.route("/new_order_type", methods=["GET", "POST"])
def new_order_type():
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_order_type.html")
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        product = request.form["product"]
        materials = request.form["materials"]
        token = request.form["csrf_token"]
        if product != "" and materials != "" and orders.add_order_type(product, materials) and \
                session["csrf_token"] == token:
            flash("Tuote lisätty listaan", "success")
            return redirect("/new_order")
        else:
            flash("Tuotteen lisääminen epäonnistui, tarkista onko tuote jo olemassa", "warning")
            return redirect(request.url)


@app.route("/new_clinic", methods=["GET", "POST"])
def new_clinic():
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            citys = customers.citys_fi()
            return render_template("new_clinic.html", citys=citys)
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        name = request.form["name"]
        adress = request.form["adress"]
        city = request.form["city"]
        postal = request.form["postal"]
        token = request.form["csrf_token"]
        if name != "" and adress != "" and postal != "" and customers.add_clinic(name, adress, postal, city) \
                and session["csrf_token"] == token:
            flash("Toimipiste lisätty listaan", "success")
            return redirect("/new_order")
        else:
            flash(
                "Toimipisteen lisääminen epäonnistui, tarkista onko toimipiste jo olemassa", "warning")
            return redirect(request.url)


@app.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("new_customer.html")
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        name = request.form["name"]
        token = request.form["csrf_token"]
        if name != "" and customers.add(name) and session["csrf_token"] == token:
            flash("Asiakas lisätty listaan", "success")
            return redirect("/new_order")
        else:
            flash(
                "Asiakkaan lisääminen epäonnistui, tarkista onko asiakas jo olemassa", "warning")
            return redirect(request.url)


@app.route("/production", methods=["GET", "POST"])
def production():
    today = date.today()
    order_list = orders.order_list(today.strftime("%Y-%m-%d"))
    if request.method == "GET":
        if users.user_status() == 1 or users.user_status() == 0:
            return render_template("production.html", date=today, order_list=order_list, today=today)
        else:
            return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")
    if request.method == "POST":
        datef = request.form["date"]
        if (datef == ""):
            return render_template("production.html", date=today, order_list=order_list, today=today)
        new_date = datetime.datetime.strptime(datef, "%Y-%m-%d").date()
        new_order_list = orders.order_list(datef)
        token = request.form["csrf_token"]
        if session["csrf_token"] == token:
            return render_template("production.html", date=new_date, order_list=new_order_list, today=today)
        else:
            return render_template("error.html", message="")


@app.errorhandler(404)
def error(e):
    return render_template("error.html")


@app.errorhandler(500)
def server_error(e):
    return redirect("/")


@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", message="Käyttäjän oikeudet eivät riitä tähän toimintoon.")

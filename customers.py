from db import db
from flask import session

# Seek all clinics where a spesific customer is related to


def clinic_list_by_customer(customer_id):
    try:
        sql = "SELECT DISTINCT ON(C.id) C.id, C.name, C.adress, C.city from orders O LEFT JOIN clinics C ON O.clinic_id=C.id LEFT JOIN customers CS ON CS.id=O.customer_id WHERE CS.id=:id"
        result = db.session.execute(sql, {"id": customer_id})
        clinic_list = result.fetchall()
        return clinic_list
    except:
        return None


def clinic_list():
    try:
        sql = "SELECT id, name, adress, postal_code, city FROM clinics ORDER BY name"
        result = db.session.execute(sql)
        clinic_list = result.fetchall()
        return clinic_list
    except:
        return None


def add_clinic(name, adress, postal_code, city):
    #First check if the clinic already exists
    clinics = clinic_list()
    for clinic in clinics:
        if name.lower() == clinic[1].lower() and adress.lower() == clinic[2].lower() and postal_code.lower() == clinic[3].lower() and city == clinic[4]:
            return False
    try:
        sql = "INSERT INTO clinics (name, adress, postal_code, city) VALUES (:name, :adress, :postal_code, :city)"
        db.session.execute(
            sql, {"name": name, "adress": adress, "postal_code": postal_code, "city": city})
        db.session.commit()
        return True
    except:
        return False


def customer_list():
    try:
        sql = "SELECT id, name FROM customers ORDER BY name"
        result = db.session.execute(sql)
        customer_list = result.fetchall()
        return customer_list
    except:
        return None

def seek(name):
    try:
        sql = "SELECT * FROM customers WHERE name ILIKE :name"
        result = db.session.execute(sql, {"name":name})
        customer = result.fetchone()
        if customer == None:
            return False
        else:
            return True
    except:
        return False


def add(name):
    #Check if customer exists
    if (seek(name)):
        return False
    try:
        sql = "INSERT INTO customers (name, visible) VALUES (:name, 1)"
        db.session.execute(sql, {"name": name})
        db.session.commit()
        return True
    except:
        return False




def citys_fi():
    try:
        sql = "SELECT * FROM citys_fi"
        result = db.session.execute(sql)
        citys_fi = result.fetchall()
        return citys_fi
    except:
        return None

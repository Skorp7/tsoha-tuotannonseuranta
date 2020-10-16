from db import db
from flask import session


def add(order_type_id, customer_id, delivery_date, clinic_id):
    try:
        sql = "INSERT INTO orders (order_type_id, customer_id, clinic_id, delivery_date, time, in_progress) " \
            "VALUES (:order_type_id, :customer_id, :clinic_id, :delivery_date, LOCALTIMESTAMP, 1) RETURNING id"
        result = db.session.execute(sql, {"order_type_id": order_type_id, "customer_id": customer_id, \
                "clinic_id": clinic_id, "delivery_date": delivery_date})
        latest_id = result.fetchone()[0]
        db.session.commit()
        return latest_id
    except:
        return None


def add_order_type(product_type, main_materials):
    order_types = order_type_list()
    for type in order_types:
        if product_type.lower() == type[1].lower() and main_materials.lower() == type[2].lower():
            return False
    try:
        sql = "INSERT INTO order_types (product_type, main_materials) VALUES (:product_type, :main_materials)"
        db.session.execute(sql, {"product_type": product_type, "main_materials": main_materials})
        db.session.commit()
        return True
    except:
        return False


def order_type_list():
    sql = "SELECT id, product_type, main_materials FROM order_types ORDER BY product_type"
    result = db.session.execute(sql)
    order_type_list = result.fetchall()
    return order_type_list


def order_list(date):
    sql = "SELECT O.id, O.order_type_id, OT.product_type, OT.main_materials, O.customer_id, " \
        "C.name, O.clinic_id, CL.name, CL.city, O.delivery_date, O.time, O.in_progress FROM orders O " \
        "LEFT JOIN customers C on C.id=O.customer_id LEFT JOIN order_types OT on OT.id=O.order_type_id "\
        "LEFT JOIN clinics CL ON CL.id=O.clinic_id  WHERE O.delivery_date::text LIKE :date ORDER BY O.delivery_date"
    result = db.session.execute(sql, {"date": date+"%"})
    order_list = result.fetchall()
    return order_list


def listAll():
    sql = "SELECT O.id, O.order_type_id, OT.product_type, OT.main_materials, O.customer_id, C.name, " \
        "O.clinic_id, CL.name, CL.city, O.delivery_date, O.time, O.in_progress, CL.adress, CL.postal_code "\
        "FROM orders O LEFT JOIN customers C on C.id=O.customer_id LEFT JOIN order_types OT on OT.id=O.order_type_id "\
        "LEFT JOIN clinics CL ON CL.id=O.clinic_id ORDER BY O.id"
    result = db.session.execute(sql)
    order_list = result.fetchall()
    return order_list


# check out: inprogress = 0
# check in: inprogress = 1
def check_out_in(order_id, in_progress):
    try:
        sql = "UPDATE orders SET in_progress=:in_progress WHERE id=:id"
        db.session.execute(sql, {"in_progress": in_progress, "id": order_id})
        db.session.commit()
        return True
    except:
        return False


def seek(order_id):
    sql = "SELECT * FROM orders WHERE id=:id"
    result = db.session.execute(sql, {"id": order_id})
    order_data = result.fetchall()
    return order_data


#Find all order information which include a part of the search word
def seekAll(word):
    if (word == None):
        return None
    sql = "SELECT O.id, O.order_type_id, OT.product_type, OT.main_materials, O.customer_id, C.name, " \
        "O.clinic_id, CL.name, CL.city, O.delivery_date, O.time, O.in_progress FROM orders O LEFT JOIN " \
        "customers C on C.id=O.customer_id LEFT JOIN order_types OT on OT.id=O.order_type_id LEFT JOIN " \
        "clinics CL ON CL.id=O.clinic_id WHERE CL.name ILIKE :word OR CL.city ILIKE :word OR C.name ILIKE :word "\
        "OR OT.product_type ILIKE :word OR OT.main_materials ILIKE :word ORDER BY O.delivery_date DESC"
    result = db.session.execute(sql, {"word": '%'+word+'%'})
    o_data = result.fetchall()
    return o_data


def amount_orders_list():
    sql = "SELECT ot.product_type, count(*) FROM orders o LEFT JOIN " \
        "order_types ot ON o.order_type_id=ot.id GROUP BY ot.product_type ORDER BY count"
    result = db.session.execute(sql)
    am_orders = result.fetchall()
    return am_orders
    

def fav_customers():
    sql = "SELECT C.name, count(*) FROM Orders O LEFT JOIN Customers C ON C.id=O.customer_id "\
        " GROUP BY C.name ORDER BY count DESC"
    result = db.session.execute(sql)
    fav_customer_list = result.fetchall()
    return fav_customer_list

from db import db
from flask import session

def add(order_id, user_id, description, is_pending):
    try:
        sql = "INSERT INTO events (order_id, user_id, description, time, is_pending) VALUES (:order_id, :user_id, :description, LOCALTIMESTAMP, :is_pending)"
        db.session.execute(sql, {"order_id":order_id, "user_id":user_id, "description":description, "is_pending":is_pending})
        db.session.commit()
        return True
    except:
        return False


def set_pending(event_id, is_pending):
    try:
        sql = "UPDATE events SET is_pending=:is_pending WHERE id=:id"
        db.session.execute(sql, {"is_pending":is_pending,"id":event_id})
        db.session.commit()
        return True
    except:
        return False

def hard_workers():
    try:
        sql = "SELECT count(*), E.user_id, U.name FROM events E LEFT JOIN Users U ON U.id=E.user_id GROUP BY E.user_id, U.name ORDER BY count(*) DESC"
        result = db.session.execute(sql)
        hard_worker_list = result.fetchall()
        return hard_worker_list
    except:
        return None



def event_list():
    try:
        sql = "SELECT E.order_id, E.user_id, E.description, E.time, E.is_pending, U.name FROM events E LEFT JOIN users U ON U.id = E.user_id ORDER BY E.time DESC"
        result = db.session.execute(sql)
        order_type_list = result.fetchall()
        return order_type_list
    except:
        return None

def list(order_id):
    try:
        sql = "SELECT E.order_id, E.user_id, U.name, E.time, E.is_pending, E.description, O.order_type_id FROM events E LEFT JOIN users U ON E.user_id=U.id LEFT JOIN Orders O ON E.order_id=O.id WHERE E.order_id=:order_id ORDER BY E.time"
        result = db.session.execute(sql, {"order_id":order_id})
        order_list = result.fetchall()
        return order_list
    except:
        return None
 


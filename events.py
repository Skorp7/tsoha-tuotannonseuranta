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



def event_list():
    try:
        sql = "SELECT * FROM events ORDER BY order_id"
        result = db.session.execute(sql)
        order_type_list = result.fetchall()
        return order_type_list
    except:
        return None

def list(order_id):
    try:
        sql = "SELECT * FROM events E LEFT JOIN users U ON E.user_id=U.id LEFT JOIN Orders O ON E.order_id=O.id"
        result = db.session.execute(sql, {"date":date+"%"})
        order_list = result.fetchall()
        return order_list
    except:
        return None
 



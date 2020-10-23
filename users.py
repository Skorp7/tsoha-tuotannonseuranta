from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password, id, status FROM users WHERE name ILIKE :name"
    result = db.session.execute(sql, {"name": username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["user_status"] = user[2]
            return True
        else:
            return False


def seek(username):
    sql = "SELECT * FROM Users WHERE name ILIKE :name"
    result = db.session.execute(sql, {"name": username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        return True


def logout():
    del session["user_id"]
    del session["user_status"]


def register(username, password):
    if seek(username):
        return False
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name,status,password,visible) VALUES (:name,99,:password, 1)"
        db.session.execute(sql, {"name": username, "password": hash_value})
        db.session.commit()
        return True
    except:
        return False


def user():
    usr_id = session.get("user_id", 0)
    sql = "SELECT id, name, status FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": usr_id})
    user_data = result.fetchone()
    return user_data


def userById(id):
    sql = "SELECT id, name, status FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    user_data = result.fetchone()
    return user_data


#This is almost duplicate but more clear, since it is used so much
#This is used instead of session.get("user_status"), because this checks every time 
#if status has changed since last login
def user_status():
    usr_id = session.get("user_id", 0)
    sql = "SELECT status FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": usr_id})
    status = result.fetchone()[0]
    return status


def update_status(user_id, new_status):
    try:
        sql = "UPDATE users SET status=:status WHERE id=:id"
        db.session.execute(sql, {"status": new_status, "id": user_id})
        db.session.commit()
        return True
    except:
        return False


def user_list():
    sql = "SELECT id, name, status FROM users ORDER BY name"
    result = db.session.execute(sql)
    user_list = result.fetchall()
    return user_list
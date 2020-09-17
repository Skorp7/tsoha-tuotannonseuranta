from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash



def login(username,password):
    sql = "SELECT password, id FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            return True
        else:
            return False

def logout():
    logged_in = None
    del session["user_id"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name,status,password,visible) VALUES (:name,0,:password, 1)"
        db.session.execute(sql, {"name":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def user_status():
    id = session.get("user_id",0)
    sql = "SELECT status FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    status = result.fetchone()[0]
    return status

def update_status(username, new_status):
    try:
        sql = "UPDATE users SET status=:status WHERE name=:name"
        db.session.execute(sql, {"status":new_status,"name":username})
        db.session.commit()
        return True
    except:
        return False

def user_list():
    try:
        sql = "SELECT name, status FROM users ORDER BY name"
        result = db.session.execute(sql)
        user_list = result.fetchall()
        return user_list
    except:
        return None
    

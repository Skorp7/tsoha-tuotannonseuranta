from db import db

def add_visit():
    db.session.execute("INSERT INTO visitors (time) VALUES (NOW())")
    db.session.commit()

def get_counter():
    result = db.session.execute("SELECT COUNT(*) FROM users")
    counter = result.fetchone()[0]
    return counter


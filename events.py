from db import db
from flask import session


def add(order_id, user_id, description, is_pending):
    try:
        sql = "INSERT INTO events (order_id, user_id, description, time, is_pending) VALUES "\
            "(:order_id, :user_id, :description, LOCALTIMESTAMP, :is_pending)"
        db.session.execute(sql, {"order_id": order_id, "user_id": user_id,
                                 "description": description, "is_pending": is_pending})
        db.session.commit()
        return True
    except:
        return False


def hard_workers():
    sql = "SELECT count(*), E.user_id, U.name FROM events E LEFT JOIN Users U ON U.id=E.user_id GROUP BY" \
        " E.user_id, U.name ORDER BY count(*) DESC"
    result = db.session.execute(sql)
    hard_worker_list = result.fetchall()
    return hard_worker_list


def event_list():
    sql = "SELECT E.order_id, E.user_id, E.description, E.time, E.is_pending, U.name FROM events E "\
        "LEFT JOIN users U ON U.id = E.user_id ORDER BY E.time DESC"
    result = db.session.execute(sql)
    order_type_list = result.fetchall()
    return order_type_list


# FIND THE QUEUE DURATIONS BY EVENT DESCRIPTION:
# Take all events, group them by order_id, remain all rows where order_id, description are the same and is_pending
# is different. So we find the pairs when an order has went to queue and when taken to handling.
# Calculate differences between times and take average of them. Group by event description.
def queue_durations():
    sql = "SELECT avg(D.diff) AS average, D.descr FROM "\
        "(SELECT (a.time-b.time) as diff, A.description as descr FROM "\
        "(SELECT * FROM (SELECT DISTINCT ON(order_id, description, is_pending)order_id, description, "\
        "is_pending, time FROM events GROUP BY order_id, description, is_pending, time ORDER BY order_id, "\
        "description, is_pending) E ORDER BY E.order_id, E.time) A, "\
        "(SELECT * FROM (SELECT DISTINCT ON(order_id, description, is_pending)order_id, description, "\
        "is_pending, time FROM events GROUP BY order_id, description, is_pending, time ORDER BY "\
        "order_id, description, is_pending) E ORDER BY E.order_id, E.time) B "\
        "WHERE A.order_id IS NOT DISTINCT FROM B.order_id AND A.is_pending IS DISTINCT FROM B.is_pending "\
        "AND A.description IS NOT DISTINCT FROM B.description) D "\
        "WHERE D.diff > time'00:00:00.000000' GROUP BY D.descr ORDER BY average DESC"
    result = db.session.execute(sql)
    duration_list = result.fetchall()
    return duration_list


# find most used event descriptions
def common_events():
    sql = "SELECT description, count(*) FROM events WHERE description != 'Sisäänkirjaus' AND "\
        "description != 'Uloskirjaus' GROUP BY description ORDER BY count DESC"
    result = db.session.execute(sql)
    description_list = result.fetchall()
    return description_list

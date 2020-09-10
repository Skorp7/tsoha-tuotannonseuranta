from app import app
from flask import render_template
import visits 


@app.route("/")
def index():
    visits.add_visit()
    counter = result.fetchone()[0]
    return render_template("index.html", counter=counter) 
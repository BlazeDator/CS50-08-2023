import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # "Get" form inputs
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")
        # For editing
        id = request.form.get("id")
        # Check user input violation
        if not name or (int(day) < 0 or int(day) > 31)  or (int(month) < 0 or int(month) > 12):
            # ERROOOOR, send error trough url
            return redirect("/?error=Erroneous inputs")
        # If no errors, check if adding value or editing
        if id:
            db.execute("UPDATE birthdays SET name=?, day=?, month=? WHERE id=?", name, day, month, id)
            return redirect("/")
        else:
            db.execute("INSERT INTO birthdays (name, day, month) VALUES (?, ?, ?)", name, day, month)
            return redirect("/")

    else:
        id = request.args.get("id") # Save id and send through
        error = request.args.get("error") # Save error and send through
        birthdays = db.execute("SELECT id, name, month, day FROM birthdays")
        return render_template("index.html", birthdays=birthdays, error=error, id=id)

@app.route("/delete", methods=["POST"])
def delete():
    # Check for ID button choosen, and delete selected entry in database
    id = request.form.get("id")
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")

@app.route("/edit", methods=["POST"])
def edit():
    id = request.form.get("id") # Get id then tell user to update and send id to the page
    return redirect("/?error=Edit active, write new values here&id="+id)


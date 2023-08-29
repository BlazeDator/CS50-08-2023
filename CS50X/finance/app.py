import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Get current user assets
    info = db.execute("SELECT * FROM assets WHERE user_id=? ORDER BY symbol ASC", session.get("user_id"))

    # Check if there is values
    if len(info) > 0:
        # Get user cash
        cash = db.execute("SELECT cash FROM users WHERE id=?", session.get("user_id"))
        cash = cash[0]["cash"]

        # Total assets
        total = cash

        # Create a new dictionary to save assets share price and holdings total
        prices = {}
        holdings = {}

        for row in info:  # For every row in assets

            # Lookup current company share price
            price = lookup(row["symbol"])

            # Save only the value for easier use
            price = price["price"]

            # Create a new key with the price
            prices[row["symbol"]] = price

            # Create a new key with the shares * share price
            holding = row["shares"] * price
            holdings[row["symbol"]] = holding

            # Add holding value to total
            total += holdings[row["symbol"]]

            # Apply USD filter
            prices[row["symbol"]] = usd(prices[row["symbol"]])
            holdings[row["symbol"]] = usd(holdings[row["symbol"]])

        # Apply USD filter
        cash = usd(cash)
        total = usd(total)

        return render_template("index.html", info=info, prices=prices, cash=cash, total=total, holdings=holdings)
    else:
        return render_template("indexnope.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)

        # Ensure symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("symbol not found", 400)

        # Ensure a number was submitted
        elif not request.form.get("shares"):
            return apology("must provide amount of shares", 400)

        # Ensure it's an integer
        elif not request.form.get("shares").isdigit():
            return apology("Use integers", 400)

        # Ensure it's a positive
        elif int(request.form.get("shares")) < 1:
            return apology("must provide a positive number of shares", 400)

        # Lookup symbol through helper function and save it
        symbol = lookup(request.form.get("symbol"))

        # Assess current user cash
        ccash = db.execute("SELECT cash FROM users WHERE id=?", session.get("user_id"))
        ccash = ccash[0]["cash"]

        # Amount of shares
        shares = int(request.form.get("shares"))

        # Check if user has enough cash
        if symbol["price"] * shares > ccash:
            return apology("Not enough cashmoney", 400)

        # Total shares price
        price = symbol["price"] * shares

        # Check if user already has assets
        assets = db.execute("SELECT * FROM assets WHERE symbol = ? AND user_id = ?", symbol["symbol"], session.get("user_id"))

        if len(assets) > 0:  # Update Assets
            # Get current shares
            current_shares = assets[0]["shares"]
            # Add new shares
            current_shares += shares
            # Update shares
            db.execute("UPDATE assets SET shares = ? WHERE symbol = ? AND user_id = ?",
                       current_shares, symbol["symbol"], session.get("user_id"))
        else:  # Add new Assets
            db.execute("INSERT INTO assets (symbol, shares, user_id) VALUES (?,?,?)",
                       symbol["symbol"], shares, session.get("user_id"))

        # Create a transaction report
        db.execute("INSERT INTO transactions (ttype, symbol, shares, tcash, user_id) VALUES ('buy', ?, ?, ?, ?)",
                   symbol["symbol"], shares, price, session.get("user_id"))

        # Update user's cash
        ccash -= price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", ccash, session.get("user_id"))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    # Get current user transactions
    info = db.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY ttime DESC", session.get("user_id"))

    sharep = {}

    for row in info:
        sharep[row["symbol"]] = row["tcash"] / row["shares"]
        sharep[row["symbol"]] = usd(sharep[row["symbol"]])

    if len(info) > 0:
        return render_template("history.html", info=info, sharep=sharep)
    else:
        return render_template("historynope.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)

        # Ensure symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("symbol not found", 400)

        # Lookup symbol through helper function and save it
        symbol = lookup(request.form.get("symbol"))
        price = symbol["price"]
        price = usd(price)

        # Render quoted.html and send symbol dictionary
        return render_template("quoted.html", symbol=symbol, price=price)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)

        # Ensure both passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Save username for easier comparison and use
        name = request.form.get("username")

        # Query database for current users
        users = db.execute("SELECT username FROM users WHERE username LIKE ?", name)

        # If username already exists warn current user
        if len(users) > 0:
            return apology("User already exists", 400)

        # Save hashed password of easier db insertion
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Add user and hash to db
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, password)

        # Select the newly created user
        user = db.execute("SELECT * FROM users WHERE username = ?", name)

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)

        # Ensure symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("symbol not found", 400)

        # Ensure a number was submitted
        elif not request.form.get("shares"):
            return apology("must provide amount of shares", 400)

        # Ensure it's an integer
        elif not request.form.get("shares").isdigit():
            return apology("Use integers", 400)

        # Ensure it's a positive
        elif int(request.form.get("shares")) < 1:
            return apology("must provide a positive number of shares", 400)

        # Amount of shares
        shares = int(request.form.get("shares"))

        # Lookup symbol through helper function and save it
        symbol = lookup(request.form.get("symbol"))

        # Total shares price
        price = symbol["price"] * shares

        # Get user's assets
        assets = db.execute("SELECT * FROM assets WHERE symbol = ? AND user_id = ?", symbol["symbol"], session.get("user_id"))
        current_shares = assets[0]["shares"]

        # Assess if the user owns enough shares for such endeavour
        if len(assets) > 0:
            if current_shares < shares:
                return apology("You don't own enough to sell", 400)
        else:
            return apology("You don't own any stock to sell", 400)

        # Sell assets
        current_shares -= shares
        if current_shares == 0:
            db.execute("DELETE FROM assets WHERE symbol = ? AND user_id = ?", symbol["symbol"], session.get("user_id"))
        else:
            db.execute("UPDATE assets SET shares = ? WHERE symbol = ? AND user_id = ?",
                       current_shares, symbol["symbol"], session.get("user_id"))

        # Create a transaction report
        db.execute("INSERT INTO transactions (ttype, symbol, shares, tcash, user_id) VALUES ('sell', ?, ?, ?, ?)",
                   symbol["symbol"], shares, price, session.get("user_id"))

        # Assess current user cash then update it
        ccash = db.execute("SELECT cash FROM users WHERE id=?", session.get("user_id"))
        ccash = ccash[0]["cash"]
        ccash += price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", ccash, session.get("user_id"))

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        assets = db.execute("SELECT * FROM assets WHERE user_id = ?", session.get("user_id"))
        return render_template("sell.html", assets=assets)


@app.route("/options")
@login_required
def options():
    return render_template("options.html")


@app.route("/options/password", methods=["GET", "POST"])
@login_required
def optionspass():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get old hash and save it as a simple variable for easier use
        oldpass = db.execute("SELECT hash FROM users WHERE id=?", session.get("user_id"))
        oldpass = oldpass[0]["hash"]

        # Ensure old password was submitted
        if not request.form.get("oldpassword"):
            return apology("must provide old password", 400)

        # Ensure both old passwords match
        elif not check_password_hash(oldpass, request.form.get("oldpassword")):
            return apology("old password must match to account's password", 400)

        # Ensure new password was submitted
        elif not request.form.get("newpassword"):
            return apology("must provide a new password", 400)

        # Ensure new password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide a confirmation password", 400)

        # Ensure both new passwords match
        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("new passwords must match", 400)

        # Save hashed password of easier db insertion
        password = generate_password_hash(request.form.get("newpassword"), method='pbkdf2:sha256', salt_length=8)

        # Update db with new password
        db.execute("UPDATE users SET hash = ?", password)

        return redirect("/options")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/options")


@app.route("/options/cash", methods=["GET", "POST"])
@login_required
def optionscash():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a number was submitted
        if not request.form.get("cash"):
            return apology("Must provide amount of cash", 400)

        # Ensure it's an integer
        elif not request.form.get("cash").isdigit():
            return apology("Only accept dollars as minimum, no cents", 400)

        # Ensure it's a positive
        elif int(request.form.get("cash")) < 1:
            return apology("Must provide a positive number of cash", 400)

        # Save cash into variable for easier use
        cash = int(request.form.get("cash"))

        # Update db with new amount of cash
        db.execute("UPDATE users SET cash = cash + ?", cash)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/options")
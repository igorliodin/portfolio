import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Get username
def getuser():
    row = db.execute("SELECT * FROM users WHERE id=:id;", id=session["user_id"])
    return row[0]['username']

# Transactions table update function
def transaction_update(user, symbol, quantity, price, transaction_type):
    db.execute("INSERT INTO transactions (user, symbol, quantity, price, type, date) VALUES (:user, :symbol, :quantity, :price, :transaction_type, CURRENT_TIMESTAMP)",
               user=user, symbol=symbol, quantity=quantity, price=price, transaction_type=transaction_type)

# Cash update function
def cash_update(user, price, transaction_type):
    # Get current cash amount, update depending on transaction type
    row = db.execute("SELECT cash FROM users WHERE id=:id;", id=session["user_id"])
    cash = row[0]['cash']
    cash = round(cash, 2)
    price = round(price, 2)

    if transaction_type == "BUY":
        db.execute("UPDATE users SET cash=:cash WHERE username=:user",
                   cash=cash-price, user=user)
    else:
        db.execute("UPDATE users SET cash=:cash WHERE username = :user",
                   cash=cash+price, user=user)

# Shares quantity update function
def shares_update(user, symbol, quantity, transaction_type):
    # Get current amount of shares for symbol
    row = db.execute("SELECT * FROM shares_table WHERE user=:user AND symbol=:symbol;", user=user, symbol=symbol)
    shares_old = int(row[0]['quantity'])
    share_id = row[0]['id']

    if transaction_type == "SELL":
        db.execute("UPDATE shares_table SET quantity=:quantity WHERE id=:id;",
                   quantity=(shares_old-quantity), id=share_id)
    elif transaction_type == "BUY":
        db.execute("UPDATE shares_table SET quantity=:quantity WHERE id=:id;",
                   quantity=(shares_old+quantity), id=share_id)


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    if request.method == "GET":
        user = getuser()
        shares = db.execute("SELECT * FROM shares_table WHERE user=:user AND quantity>0 ORDER BY symbol", user=user)
        tmp = db.execute("SELECT * FROM users WHERE username=:user", user=user)
        cash = tmp[0]['cash']
        grand = cash
        stats = []

        # error check
        if not user:
            return apology("not found in db", 403)

        # condition for no shares for current user
        elif not shares:
            stats = [{'symbol': "None", 'name': "-", 'quantity': "-", 'price': 0.0, 'total': 0.0}]
            return render_template("index.html", stats=stats, cash=cash, grand=grand)

        # if shares found:
        else:

            # Calculate the price of existing shares for user
            for row in shares:
                tmpdict = {}
                quote = lookup(row['symbol'])
                if not quote:
                    return apology("API error", 403)
                symbol = row['symbol']
                total = quote['price'] * row['quantity']
                name = quote['name']
                price = quote['price']
                quantity = row['quantity']
                grand += total
                tmpdict['symbol'] = symbol
                tmpdict['name'] = name
                tmpdict['quantity'] = quantity
                tmpdict['price'] = price
                tmpdict['total'] = total

                # add info to stats
                stats.append(tmpdict)

            return render_template("index.html", cash=cash, stats=stats, grand=grand)

    else:
        return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("enter symbol", 403)
        shares = request.form.get("shares")
        if not shares:
            return apology("enter the number of shares", 403)
        elif not shares.isdigit:
            return apology("invalid entry", 403)
        elif int(shares) < 1:
            return apology("invalid number of shares", 403)
        transaction_type = "BUY"
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("no quote", 403)

        # creating table for transactions
        try:
            transactions = db.execute(
                "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY UNIQUE, user TEXT NOT NULL, symbol TEXT, quantity INTEGER, price MONEY, type TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);")
            shares_table = db.execute(
                "CREATE TABLE IF NOT EXISTS shares_table (id INTEGER PRIMARY KEY UNIQUE, user TEXT NOT NULL, symbol TEXT, quantity INTEGER);")
        except:
            return apology("table creation error", 403)
        if not transactions or not shares_table:
            return apology("database insertion error", 403)

        # check for available funds
        user = getuser()
        row = db.execute("SELECT * FROM users WHERE username=:user;", user=user)
        cash = float(row[0]['cash'])

        # calculate transaction amount
        transaction_amount = float(quote["price"]) * int(shares)
        if cash < transaction_amount:
            return apology("insufficient funds", 403)

        else:
            # check if the user already has shares of current symbol in shares_table
            check_shares = db.execute("SELECT * FROM shares_table WHERE symbol=:symbol AND user=:user;",
                                      user=user, symbol=symbol)

            # add to db if no shares found
            if not check_shares:
                try:
                    add = db.execute("INSERT INTO shares_table (user, symbol, quantity) VALUES (:user, :symbol, :quantity);",
                                     user=user, symbol=symbol, quantity=shares)
                except:
                    return apology("error", 403)
                if not add:
                    return apology("database insertion error", 403)
                else:
                    transaction_update(user, symbol, shares, transaction_amount, transaction_type)
                    cash_update(user, transaction_amount, transaction_type)

            # if shares found, update
            else:
                shares = int(shares)
                shares_update(user, symbol, shares, transaction_type)
                if not shares_update:
                    return apology("database update error", 403)
                else:
                    transaction_update(user, symbol, shares, transaction_amount, transaction_type)
                    cash_update(user, transaction_amount, transaction_type)

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    if request.method == "GET":

        # get transactions history for user
        user = getuser()
        history = db.execute("SELECT * FROM transactions WHERE user=:user ORDER BY date", user=user)

        # error check
        if not history:
            history = [{'id': "N/A", 'type': "N/A", 'symbol': "N/A", 'quantity': 0, 'price': 0.0, 'date': "N/A"}]
            return render_template("history.html", history=history)
        else:
            return render_template("history.html", history=history)

    else:
        return render_template("history.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Get stock quote."""

    # condition for POST method
    if request.method == "POST":

        # check for empty symbol field
        if request.form.get("symbol") == None:
            return apology("symbol not provided", 403)

        else:
            # get the price for the symbol submitted
            quote = lookup(request.form.get("symbol"))

            # check if the stock exists
            if not quote:
                return apology("stock doesn't exist", 403)

            return render_template("quoted.html", name=quote["name"], price=quote["price"])

    # condition for GET method
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # condition for POST method
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Ensure password confirmation is equal to password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation don't match", 403)

        # Submit new user into database
        try:
            registration = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash);",
                                      username=request.form.get("username"),
                                      hash=generate_password_hash(request.form.get("password")))
            transactions = db.execute(
                "CREATE TABLE IF NOT EXISTS transactions (id integer PRIMARY KEY, user text NOT NULL, symbol, quantity, price, type, date, time);")

        except:
            return apology("user already exists", 403)

        if not registration or not transactions:
            return apology("database insertion error", 403)

        session["user_id"] = registration

        # Redirect user to home page
        return redirect("/")

    # condition for GET method
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user = getuser()
    symbols = db.execute("SELECT symbol FROM shares_table WHERE user=:user;", user=user)
    transaction_type = "SELL"
    if not symbols:
        return apology("Stock shares unavailable", 403)

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # error check
        if not symbol:
            return apology("symbol not selected", 403)
        if not shares:
            return apology("no shares entered", 403)
        elif int(shares) < 1:
            return apology("enter number of shares > 1", 403)

        else:
            shares = int(shares)

            # get quote for symbol
            quote = lookup(symbol)

            if not quote:
                return apology("invalid symbol", 403)

            # get transaction price
            price = quote["price"] * shares

            # get user shares
            get_shares = db.execute("SELECT * FROM shares_table WHERE user=:user AND symbol=:symbol",
                                    user=user, symbol=symbol)
            user_shares = get_shares[0]['quantity']

            # check for shares availability
            if int(user_shares) < shares:
                return apology("not enough shares", 403)

            else:
                # update user cash in users
                cash_update(user, price, transaction_type)

                # update transactions
                transaction_update(user, symbol, shares, price, transaction_type)

                # update shares_table
                shares_update(user, symbol, shares, transaction_type)

        # Redirect to homepage
        return redirect("/")

    else:
        return render_template("sell.html", symbols=symbols)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """Top up cash"""

    row = db.execute("SELECT * FROM users WHERE id=:id;", id=session["user_id"])
    user = row[0]['username']

    if request.method == "POST":

        # check if input is valid
        if not request.form.get("amount"):
            return apology("amount not entered", 403)
        elif float(request.form.get("amount")) < 0.01:
            return apology("enter valid amount", 403)

        # add funds
        else:
            amount = float(request.form.get("amount"))
            transaction_type = "ADD"
            cash_update(user, amount, transaction_type)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("topup.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

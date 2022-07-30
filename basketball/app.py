import os
from flask import Flask
from flask import render_template,request,session,redirect,flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps
from datetime import timedelta
from flask_mail import Mail, Message



db=SQL("sqlite:///basketball.db")

app=Flask(__name__)





app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.permanent_session_lifetime = timedelta(minutes=2)
Session(app)



def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function




@app.route("/")
def index():
        return render_template("about.html")

@app.route("/login", methods=["GET","POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username=request.form.get("username")
        if not username:
           flash("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")


        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        if len(rows) != 1 or len(rows)==None or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash ("Invalid password or username")
            return render_template("login.html")



        session["user_id"]=rows[0]["id"]

        flash("Welcome " +  username.title())


        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        if not request.form.get("username"):
            flash("Username is required")
            return render_template("register.html")

        elif not request.form.get("password"):
            flash("Password is required")
            return render_template("register.html")

        elif not request.form.get("confirmation"):
            flash("Confirm password is required")
            return render_template("register.html")

        elif not request.form.get("email"):
           flash("Email is required")
           return render_template("register.html")

        elif not request.form.get("phonenumber"):
            flash("Phone number is required")
            return render_template("register.html")

        elif not request.form.get("birthday"):
            flash("Birthday is required")
            return render_template("register.html")

        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("faliure.html")


        hash=generate_password_hash(request.form.get("password"))
        email=request.form.get("email")
        phonenumber=request.form.get("phonenumber")
        birthday=request.form.get("birthday")

        try:
            new_user=db.execute("INSERT INTO users(username,hash,email,phonenumber,birthday)VALUES(?,?,?,?,?)",username,hash,email,phonenumber,birthday)
        except:
            flash("Username Aready exists")
            return render_template("register.html")


        session["user_id"]=new_user
        flash("welcome" + username.upper())



        return redirect("/appointments")



    else:
        return render_template("register.html")

@app.route("/logout")
def logout():


    session.clear()


    return redirect("/login")

@app.route("/admin")
@login_required
def admin():
        session["user_id"]
        scheduleall=db.execute("SELECT * from appointments")
        return render_template("admin.html",scheduleall=scheduleall)



@app.route("/appointments",methods=["GET","POST"])
@login_required
def appointments():
    user_id=session["user_id"]
    if request.method=="POST":
        time=request.form.get("time")
        name=request.form.get("name")


        if not name:
            flash("Should provide email")
            return render_template("appointments.html")

        elif not time:
            flash("Should provide time")
            return render_template("appointments.html")


        db.execute("INSERT into appointments(user_id,name,time)VALUES(?,?,?)",user_id,name,time)


        return redirect("/schedules")


    else:
        return render_template("appointments.html")

@app.route("/schedules")
@login_required
def schedules():
    user_id=session["user_id"]
    if user_id != 1:

        schedule=db.execute("SELECT * from appointments where user_id =?",user_id)
        return render_template("schedule.html",schedule=schedule)

    else:
        scheduleall=db.execute("Select * from appointments")
        return render_template("admin.html",scheduleall=scheduleall)




@app.route("/deregister", methods=["POST"])
def deregister():
    session["user_id"]
    id = request.form.get("id")
    registrants=request.form.get("registrants")
    if id:
        db.execute("DELETE FROM appointments where name =?",id)
        return redirect("/schedules")

    if registrants:
        db.execute("DELETE FROM users where username =?",registrants)
        return redirect("/registrants")


    return render_template("appointments.html")


@app.route("/registrants")
@login_required
def registrants():
    session["user_id"]
    registrants=db.execute("SELECT * FROM users")
    return render_template("registrants.html",registrants=registrants)








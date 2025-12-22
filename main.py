from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from controller.config import Config
from controller.database import db
from controller.models import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ---------------- CREATE TABLES ----------------
with app.app_context():
    db.create_all()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]  # student / teacher

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        # ✅ AUTO LOGIN AFTER SIGNUP
        session["user_id"] = user.user_id
        session["username"] = user.username
        session["role"] = user.role

        return redirect(url_for("login_success"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.user_id
            session["username"] = user.username
            session["role"] = user.role

            return redirect(url_for("login_success"))

        flash("Invalid email or password")

    return render_template("login.html")


# ---------------- LOGIN SUCCESS (DASHBOARD) ----------------
@app.route("/login-success")
def login_success():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "login_success.html",
        username=session["username"],
        role=session["role"]
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run()

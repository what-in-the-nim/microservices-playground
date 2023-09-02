import os

import httpx
from dotenv import load_dotenv
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

load_dotenv()

# endpoints
ORDER_SERVICE_URL = "http://order_service:8001"
PRODUCT_SERVICE_URL = "http://product_service:8002"
USER_SERVICE_URL = "http://user_service:8003"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["STATIC_FOLDER"] = "static"


def _login(username, password):
    response = httpx.request(
        "POST",
        f"{USER_SERVICE_URL}/users/login?username={username}&password={password}",
    )
    return response


def _get_products():
    response = httpx.request("GET", f"{PRODUCT_SERVICE_URL}/products")
    return response


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("flowers"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Sample authentication logic (replace with API call)
    response = _login(username, password)
    success = response.status_code == 200
    if success:
        session["username"] = username
        session["is_admin"] = response.json()["is_admin"]
        return redirect(url_for("flowers"))
    else:
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for("index"))


@app.route("/flowers")
def flowers():
    if "username" in session:
        flowers = _get_products().json()
        return render_template("main.html", flowers=flowers)
    else:
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)

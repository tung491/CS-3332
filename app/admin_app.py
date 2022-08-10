from hashlib import sha512

import flask
import flask_login
from flask import Flask, flash, redirect, session
from flask_login import LoginManager, logout_user

from app.adapters.database.postgres import (PostgresSaltAdapter,
                                            PostgresAdminAdapter)
from app.core.admin.models import AdminGetOnePayload, AdminCheckPasswordPayload
from app.core.admin.services import AdminsGetOneService, AdminsCheckPasswordService
from app.core.salts.models import SaltGetOnePayload
from app.core.salts.services import SaltsGetOneService
from app.routers.admin_side import admin_app
from app.settings import Settings


def init_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Settings().dict())
    return app


login_manager = LoginManager()
app = init_app()
app.secret_key = b'_5#y2L"F4Q8z\n\2xec]sdasdasd/'
login_manager.init_app(app)

app.register_blueprint(admin_app)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        session.pop('_flashes', None)
        return flask.render_template("admin_login_form.html")
    email = flask.request.form["email"]
    password = flask.request.form["password"]
    salt_adapter = PostgresSaltAdapter()
    admin_adapter = PostgresAdminAdapter()
    salt_get_one_service = SaltsGetOneService(salt_adapter)
    admin_get_one_service = AdminsGetOneService(admin_adapter)

    admin_resp = admin_get_one_service.get_one(
            AdminGetOnePayload(
                    email=email
            )
    )
    if admin_resp.data is None:
        flash("Incorrect email or password.", "danger")
        return flask.render_template("admin_login_form.html")
    salt_resp = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=admin_resp.data.id,
            )
    )
    password_hash = sha512(f"{password}{salt_resp.salt}".encode("utf-8")).hexdigest()
    check_password_service = AdminsCheckPasswordService(admin_adapter)
    check_password_resp = check_password_service.check_password(
           AdminCheckPasswordPayload(
                    admin_id=admin_resp.data.id,
                    password=password_hash,
            )
    )
    if check_password_resp.match:
        flask_login.login_user(admin_resp.data)
        flask.flash('Logged in successfully.')
        return flask.redirect("/")
    else:
        flask.flash('Incorrect card number or PIN.', 'danger')
        return flask.render_template("admin_login_form.html")


@app.route("/logout")
@flask_login.login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    try:
        admin_adapter = PostgresAdminAdapter()
        admin_get_one_service = AdminsGetOneService(admin_adapter)
        admin_resp = admin_get_one_service.get_one(
                AdminGetOnePayload(
                        admin_id=id,
                )
        ).data
    except Exception:
        return None
    if admin_resp.is_active:
        return admin_resp
    else:
        return None

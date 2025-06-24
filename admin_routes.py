# admin_routes.py
from bottle import route
from app.controllers.application import Application

ctl = Application()

@route("/admin/add-product", method=["GET"])
def add_product():
    return ctl.render("add_product", isAdmin=True)

@route("/admin/remove-product", method=["GET"])
def remove_product():
    return ctl.render("remove_product", isAdmin=True)

@route("/admin/edit-product", method=["GET"])
def edit_product():
    return ctl.render("edit_product", isAdmin=True)

@route("/admin/view-products", method=["GET"])
def view_products():
    return ctl.render("view_products", isAdmin=True)

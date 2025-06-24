from bottle import template

class Application:

    def __init__(self):
        self.pages = {
            "initial_page": self.initial_page,
            "helper": self.helper,
            "checkout": self.checkout,
            "carrinho": self.carrinho,
            "admin": self.admin,
            "perfil": self.perfil
        }
        self.admin_pages = {
            "add_product": self.add_product,
            "remove_product": self.remove_product,
            "edit_product": self.edit_product,
            "view_products": self.view_products
        }

    def render(self, page, isAdmin=False):
        if isAdmin:
            content = self.admin_pages.get(page, self.admin_pages)
            return content()
        content = self.pages.get(page, self.helper)
        return content()

    @staticmethod
    def helper():
        return template("helper")

    @staticmethod
    def checkout():
        return template("checkout")

    @staticmethod
    def carrinho():
        return template("carrinho")

    @staticmethod
    def admin():
        return template("admin")

    @staticmethod
    def perfil():
        return template("perfil")

    @staticmethod
    def initial_page():
        return template("initial_page")

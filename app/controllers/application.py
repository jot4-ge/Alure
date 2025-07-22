from bottle import template
from app.controllers.ProductRecord import ProductRecord

class Application:

    def __init__(self):
        self.pages = {
            "initial_page": self.initial_page,
            "checkout": self.checkout,
            "carrinho": self.carrinho,
            "admin": self.admin,
            "perfil": self.perfil,
            "camisetas": self.camisetas,
            "acessorios": self.acessorios,
            "streetwear": self.streetwear,
            "login": self.login,
            "register": self.register
        }
        self.admin_pages = {
            "add_product": self.add_product,
            "remove_product": self.remove_product,
            "edit_product": self.edit_product,
            "view_products": self.view_products
        }

    def render(self, page, isAdmin=False):
        if isAdmin:
            content = self.admin_pages.get(page)
            if content is None:
                return template("admin_pages/admin_error", message=f"Página admin '{page}' não encontrada.")
            return content()
        content = self.pages.get(page)
        return content()

    @staticmethod
    def render_with_data(template_name: str, **kwargs):
        return template(template_name, **kwargs)

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

    @staticmethod
    def acessorios():
        product_db = ProductRecord()
        produtos = product_db.get_products_by_category("acessorios")
        return template("product_catalogs/acessorios", produtos=produtos)

    @staticmethod
    def camisetas():
        product_db = ProductRecord()
        produtos = product_db.get_products_by_category("camisetas")
        return template("product_catalogs/camisetas", produtos=produtos)

    @staticmethod
    def streetwear():
        product_db = ProductRecord()
        produtos = product_db.get_products_by_category("streetwear")
        return template("product_catalogs/streetwear", produtos=produtos)

    @staticmethod
    def login():
        return template("login")

    @staticmethod
    def register():
        return template("register")

    #---------------------------- admin routes ----------------------------
    @staticmethod
    def add_product():
        return template("admin_pages/add_product")

    @staticmethod
    def remove_product():
        return template("admin_pages/remove_product")

    @staticmethod
    def edit_product():
        return template("admin_pages/edit_product")

    @staticmethod
    def view_products():
        return template("admin_pages/view_products")

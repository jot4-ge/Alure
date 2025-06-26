from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            "initial_page": self.initial_page,
            "checkout": self.checkout,
            "carrinho": self.carrinho,
            "admin": self.admin,
            "perfil": self.perfil,
            "camisetas": self.camisetas,
            "acessorios": self.acessorios,
            "streetwear": self.streetwear
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

    # ---------------------------- catalogos routes ----------------------------
    @staticmethod
    def acessorios():
        return template("product_catalogs/acessorios")

    @staticmethod
    def camisetas():
        return template("product_catalogs/camisetas")

    @staticmethod
    def streetwear():
        return template("product_catalogs/streetwear")

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

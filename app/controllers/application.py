from bottle import template

class Application:

    def __init__(self):
        self.pages = {
            "initial_page": self.initial_page,
            "helper": self.helper,
            "checkout": self.checkout,
            "carrinho": self.carrinho
        }

    def render(self, page):
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
    def initial_page():
        return template("initial_page")

from bottle import template


class Application:

    def __init__(self):
        self.pages = {
            "initial_page" : self.initial_page
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    @staticmethod
    def helper():
        return template('app/views/html/helper')
    @staticmethod
    def initial_page():
        return template("app/views/html/initial_page")
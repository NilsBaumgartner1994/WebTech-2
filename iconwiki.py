from server import webserver
from iconeditor import IconEditorApp
from wiki import WikiApp
from server.apps.static import StaticApp
from server.middlewares import basicAuth
from cookies import appendDict

class IconWikiApp(webserver.App):


    cookiename = 'nightmode' #cookiename
    nightmode = 'hell' #default value

    def register_routes(self):
        self.add_route("hilfe$", self.help)
        self.add_route("settings$", self.settings)
        self.add_route("settingsSave$", self.save)

    def help(self, request, response, pathmatch):
        """Show the help page."""
        response.send_template("hilfe.tmpl", appendDict(request, {}))

    def settings(self, request, response, pathmatch):
        """Show the help page."""
        response.send_template("settings.tmpl", appendDict(request, {}))

    def save(self, request, response, pathmatch):
        """Evaluate request and construct response."""
        try:
            nightmode = request.params['nightmodebox']
        except KeyError:
            nightmode = 'hell'

        response.add_cookie(self.make_cookie(nightmode))
        response.send_redirect("/settings")

    def make_cookie(self, value):
        """Returns Cookie object for nightmode"""
        return webserver.Cookie(self.cookiename, value, path='/', expires=webserver.Cookie.expiry_date(30))

if __name__ == '__main__':
    auth = basicAuth.BasicAuthMiddleware()

    server = webserver.Webserver()
    server.set_templating("jinja2")
    server.set_templating_path("templates")

    server.add_app(IconEditorApp())
    server.add_app(WikiApp())
    server.add_app(IconWikiApp())
    server.add_app(StaticApp(prefix='static', path='static'))

    server.add_middleware(auth)
    auth.add_key("user", "pass")

    server.serve()
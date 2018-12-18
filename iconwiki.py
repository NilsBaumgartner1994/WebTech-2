from server import webserver
from iconeditor import IconEditorApp
from wiki import WikiApp
from server.apps.static import StaticApp
from server.middlewares import basicAuth

class IconWikiApp(webserver.App):

    def register_routes(self):
        self.add_route("hilfe$", self.help)

    def help(self, request, response, pathmatch):
        """Show the help page."""
        response.send_template("hilfe.tmpl")

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
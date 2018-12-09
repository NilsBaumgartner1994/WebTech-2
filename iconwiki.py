from server import webserver
from iconeditor import IconEditorApp
from wiki import WikiApp
from server.webserver import StopProcessing
from server.apps.static import StaticApp


if __name__ == '__main__':
    server = webserver.Webserver()
    server.set_templating("jinja2")
    server.set_templating_path("templates")

    server.add_app(IconEditorApp())
    server.add_app(WikiApp())
    server.add_app(StaticApp(prefix='static', path='static'))

    server.serve()
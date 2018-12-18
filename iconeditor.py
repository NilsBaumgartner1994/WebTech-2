__author__ = 'Tobias Thelen'

from server import webserver
from server.webserver import StopProcessing
from server.apps.static import StaticApp
from server.log import log
from cookies import appendDict


import os, re

class IconEditorApp(webserver.App):

    def register_routes(self):
        self.add_route("iconeditor/saveZeichner$", self.saveZeichner)
        self.add_route("iconeditor/saveFueller$", self.saveFueller)
        self.add_route("iconeditor/saveRadierer$", self.saveRadierer)
        self.add_route("iconeditor$", self.show)
        self.add_route("iconeditor/save$", self.save)

    def show(self, request, response, pathmatch):
        """Show the editor. Provide list of saved icons."""

        """Tools List"""
        tool_list = os.listdir("data/tools")
        tools_html = "<ul>"
        for tool_title in tool_list:
            if tool_title != '.DS_Store':
                with open("data/tools/" + tool_title, "r") as g:
                    tools_html += "<li class=tool-list-item><img src='%s' title='%s' id='tool-%s' border='0'></li>" % (g.read(), tool_title,tool_title)
        tools_html += "</ul>"
        """End Toolslist"""

        icon_list = os.listdir("data")
        icons_html = "<ul>"
        icons = []
        for icon_title in icon_list:
            #print(icon_title+"\n")
            if icon_title != 'tools' and icon_title != '.DS_Store':
                with open("data/"+icon_title, "r") as f:
                    print("IConTitle: "+icon_title+"\n")
                    side = "<img src='%s' title='%s'>" % (f.read(), icon_title)
                    icons.append(("", side))
                    icons_html += "<li class=icon-list-item><img src='%s' title='%s'></li>" % (f.read(), icon_title)
        icons_html += "</ul>"
        response.send_template("iconeditor.tmpl", appendDict(request,{'icons': icons_html, 'tools' : tools_html, 'sidebar':icons}))

    def saveZeichner(self, request, response, pathmatch):
        """Save Zeichner to Cookies"""
        self.saveTool(response, 1)

    def saveFueller(self, request, response, pathmatch):
        """Save Fueller to Cookies"""
        self.saveTool(response, 2)

    def saveRadierer(self, request, response, pathmatch):
        """Save Radierer to Cookies"""
        self.saveTool(response, 3)

    def saveTool(self, response, tool):
        """Save selected Tool to Cookies"""
        response.add_cookie(webserver.Cookie('icontool', tool, path='/'))  # , expires=webserver.Cookie.expiry_date(-1)))
        response.send_redirect('/iconeditor')

    def save(self, request, response, pathmatch):
        """Save base64-encoded representation of icon pixels to a file."""

        if 'title' not in request.params or \
            not re.match(r"^[a-zA-Z0-9]+$", request.params['title']) or \
            'icon' not in request.params or \
            not request.params['icon'].startswith('data:'):
            raise StopProcessing(500, "Invalid parameters")
        else:
            with open("data/"+request.params['title'], "w") as f:
                f.write(request.params['icon'])
        response.send_redirect('/iconeditor')


if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(IconEditorApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()
"""
wiki.py
A very very simple Wiki

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 3 (10/2016)
"""

from server import webserver
from server.apps.static import StaticApp
import re
import os
from cookies import appendDict
from server.log import log


class NoSuchPageError(Exception):
    """Raise if try to access non existant wiki page."""
    pass


class WikiApp(webserver.App):
    """
    Webanwendung zum kollaborativen Schreiben (wiki).

    Diese sehr einfache Anwendung demonstriert ein simples Wiki.
    """

    def register_routes(self):
        self.add_route("", self.show)
        self.add_route("show(/(?P<pagename>\w+))?", self.show)
        self.add_route("edit/(?P<pagename>\w+)", self.edit)
        self.add_route("save/(?P<pagename>\w+)", self.save)

    def read_page(self, pagename):
        """Read wiki page from data directory or raise NoSuchPageError."""

        try:
            with open("wikidata/"+pagename, "r", encoding="utf-8", newline='') as f:
                x = f.read()
                m = re.search('^(<icon>[\w\d]*</icon>)([\s\S]*)', x)
                if m == None:
                    return None, x
                icon = m.group(1)
                icon = re.sub("<icon>", "", icon)
                icon = re.sub("</icon>", "", icon)
                return icon, m.group(2)
        except IOError:
            raise NoSuchPageError

    def markup(self, text):
        """Substitute wiki markup in text with html."""

        text = re.sub(r"<",
                      r"&lt;",
                      text)

        # substitute links: [[pagename]] -> <a href="/show/pagename">pagename</a>
        text = re.sub(r"\[\[([a-zA-Z0-9]+)\]\]",
                      r"<a href='/show/\1'>\1</a>",
                      text)

        # substitute headlines: !bang -> <h1>bang</h1>
        text = re.sub(r"^!(.*)$", r"<h1>\1</h1>", text, 0, re.MULTILINE)

        # replace two ends of line with <p>
        text = re.sub(r"\r?\n\r?\n", r"<p>", text)

        # replace one end of line with <br>
        text = re.sub(r"\r?\n\r?\n", r"<br>", text)

        return text

    def getPages(self):
        page_list = os.listdir("wikidata")
        pages = []
        for page_title in page_list:
                sitepath = "/show/"+page_title
                icon, text = self.read_page(page_title)
                if not icon == None:
                    try:
                        with open("data/" + icon, "r") as f:
                            side = "<a class=icon-list-item><img src='%s' title='%s'></a> " % (f.read(), icon)
                            page_title = side + page_title
                    except IOError:
                        pass

                pages.append((sitepath, page_title))
        return pages

    def updateRecently(self, cookies, response, pagename):
        pages = []
        if "recently" in cookies:
            pages = re.split("#", cookies["recently"])
        if "" in pages:
            pages.remove("")
        if pagename in pages:
            pages.remove(pagename)
        pages.insert(0, pagename)
        if len(pages) > 4:
            pages = pages[0:4]
        cookiestring = ""
        for element in pages:
            if not element == "":
                cookiestring += element
                cookiestring += "#"
        response.add_cookie(webserver.Cookie('recently', cookiestring, path='/'))#, expires=webserver.Cookie.expiry_date(-1)))
        return pages[1:4]

    def show(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        try:
            pagename = pathmatch.group('pagename') or "main"
        except IndexError:
            pagename = "main"  # default pagename

        try:
            icon, text = self.read_page(pagename)
        except NoSuchPageError:
            # redirect to edit view if page does not exist
            response.send_redirect("/edit/" + pagename)
            return

        recently = self.updateRecently(request.cookies, response, pagename)
        recentlyLink = []
        for e in recently:
            recentlyLink.append(("/show/"+e,e))

        if icon == None:
            text = self.markup(text)
        else:
            try:
                with open("data/"+icon, "r") as f:
                    side = "<a class=icon-list-item><img src='%s' title='%s'></a> " % (f.read(), icon)
                    text = side + self.markup(text)
            except IOError:
                log(3, "Icon not found.")
                text = self.markup(text)

        # show page
        response.send_template('wiki/show.tmpl', appendDict(request, {'text': text, 'pagename': pagename, 'sidebar':self.getPages(), 'recently':recentlyLink}))

    def edit(self, request, response, pathmatch=None):
        """Display wiki page for editing."""

        try:
            pagename = pathmatch.group('pagename') or "main"
        except IndexError:
            pagename = "main"

        try:
            icon, text = self.read_page(pagename)
        except NoSuchPageError:
            # use default text if page does not yet exist
            text = "This page is still empty. Fill it."

        # fill template and show
        response.send_template('wiki/edit.tmpl', appendDict(request, {'text': text, 'pagename': pagename, 'sidebar':self.getPages()}))

    def save(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        try:
            pagename = pathmatch.group('pagename')
        except IndexError:
            # no pagename given: error
            response.send_template("wiki/wikierror.tmpl",
                                   {'error': 'No pagename given.', 'text': 'save action needs pagename'}, code=500)
            return

        try:
            wikitext = request.params['wikitext']
        except KeyError:
            # no text given: error
            response.send_template("wiki/wikierror.tmpl",
                               {'error':'No wikitext given.',
                                'text':'save action needs wikitext'}, code=500)
            return

        iconname = "a1"

        # ok, save text
        f = open("wikidata/" + pagename, "w", encoding='utf-8', newline='')
        f.write("<icon>")
        f.write(iconname)
        f.write("</icon>")
        f.write(wikitext)
        f.close()

        response.send_redirect("/show/"+pagename)


if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(WikiApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()

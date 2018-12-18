import base64
import re
from server.log import log
from server.webserver import Middleware, StopProcessing

class BasicAuthMiddleware(Middleware):
    def __init__(self):
        self.keys = {}
        super().__init__()

    def add_key(self, key, value):
        self.keys[key] = value

    def remove_key(self, key):
        del self.keys[key]

    def no_auth(self):
        log(3, "No authentication.")
        raise StopProcessing(401, "No authentication.")

    def check_key(self, authHeader):
        encKey, subs = re.subn("^Basic", "", authHeader)
        if subs == 1:
            encKey = encKey.strip()
            decKey = base64.b64decode(encKey).decode('utf-8')
            decKey = re.split(":", decKey, 1)
            if len(decKey) != 2:
                log(3, "Wrong key structure.")
                return False
            if decKey[0] not in self.keys:
                log(3, "Wrong user.")
                return False
            elif self.keys[decKey[0]] == decKey[1]:
                return True
            else:
                log(3, "Wrong password.")
        return False

    def process_request(self, request, response):
        """Get authentication from request."""

        if 'Authorization' not in request.headers:
            self.no_auth()
        elif not self.check_key(request.headers['Authorization']):
                self.no_auth()




    def process_response(self, response):
        """Respond with Error if no authentication."""
        if response.code == 401:
            log(3, "Responsecode: " + str(response.code))
            response.add_header('WWW-Authenticate', 'Basic realm=\"Bitte Passwort eingeben\"')

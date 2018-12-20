import base64
import re
from server.log import log
from server.webserver import Middleware, StopProcessing

class BasicAuthMiddleware(Middleware):
    """Basic Authenthification Middleware for security"""

    def __init__(self):
        """Init Method"""
        self.keys = {}
        super().__init__()

    def add_key(self, key, value):
        """Adds a Key to out list"""
        self.keys[key] = value

    def remove_key(self, key):
        """Removes a key from our list """
        del self.keys[key]

    def no_auth(self):
        """ Respond that no Authentification is given/there"""
        log(3, "No authentication.")
        raise StopProcessing(401, "No authentication.")

    def check_key(self, authHeader):
        """ Checks if a given authentification is valid/in our list/known"""
        encKey, subs = re.subn("^Basic", "", authHeader) #get the complete key
        if subs == 1: #if correct amount/or is there
            encKey = encKey.strip() #remove whitespaces
            decKey = base64.b64decode(encKey).decode('utf-8') #decode with base64
            decKey = re.split(":", decKey, 1) #split for 2 keys
            if len(decKey) != 2: #if not enough
                log(3, "Wrong key structure.")
                return False
            if decKey[0] not in self.keys: #check if both keys known
                log(3, "Wrong user.")
                return False
            elif self.keys[decKey[0]] == decKey[1]:
                return True #both keys where known
            else:
                log(3, "Wrong password.")
        return False

    def process_request(self, request, response):
        """Get authentication from request."""

        if 'Authorization' not in request.headers: #check if Authentification is given
            self.no_auth()
        elif not self.check_key(request.headers['Authorization']): #check if valid
                self.no_auth()

    def process_response(self, response):
        """Respond with Error if no authentication."""
        if response.code == 401:
            log(3, "Responsecode: " + str(response.code))
            response.add_header('WWW-Authenticate', 'Basic realm=\"Bitte Passwort eingeben\"')

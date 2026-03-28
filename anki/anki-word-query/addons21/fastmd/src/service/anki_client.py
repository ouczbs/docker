from .http import *
class AnkiClient(Http):
    def __init__(self, session):
        Http.__init__(self, session)
        self.url = 'http://127.0.0.1:8765'
        self.version = None
    def api(self, data):
        if self.version:
            data["version"] = self.version
        data = json.dumps(data)
        res = self._post(self.url, data)
        return json.loads(res)
    def make_version(self):
        self.version = self.api({"action":"version"})
        return self.version
    def deckNames(self):
        return self.api({"action":"deckNames"})
    def modelNames(self):
        return self.api({"action":"modelNames"})
    def modelFieldNames(self, modelName):
        return self.api({"action":"modelFieldNames", "params" :{"modelName" : modelName}})
    def addNote(self, note):
        return self.api({"action":"addNote", "params" : {"note": note}})
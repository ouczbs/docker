import json, requests
import  http.cookiejar as cookielib
#from utils import singleton
class Session(requests.Session):
    def __init__(self,headers={},cookie_file=None):
        requests.Session.__init__(self)
        self.cookies = cookielib.LWPCookieJar(filename=cookie_file)
        try:self.cookies.load(ignore_discard=True)
        except Exception as e:print(e,"failed load cookie_file")
        self.headers=headers
        self.auth = ('user', 'pass')
        self._type='str'
    def save(self):
        self.cookies.save()
class Http():
    def __init__(self , session):
        self.session = session
    def _get(self, url, data = None):
        r = self.session.get(url, params = data)
        self._error(r.status_code,url)
        return self._res_data(r,self.session._type)
        
    def _post(self, url, data):
        r = self.session.post(url, data = data)
        self._error(r.status_code, url)
        return self._res_data(r, self.session._type)
        
    def _error(self, code, url):
        if code==200:return
        elif code==403:raise RuntimeError('403 - Forbidden '+url)
        elif code==404:raise RuntimeError('404 -  Not Found '+url)
        
    def _res_data(self, res, _type):
        if _type=='json':return json.loads(res.content)
        return res.content
import json
import hashlib
from requests import Request, Session

class RouterApi():
    """Interacts with the Frontier router's API"""
    def __init__(self, routerAddress, routerPassword):   
        """ Set up """
        self.session = Session()     
        self.headers = {}
        self.cookies = {}
        self.passwordSalt = ""
        self.routerPassword = routerPassword
        self.urlRouter = routerAddress
        self.urlLogin = "{0}/api/login".format(self.urlRouter)
        self.urlLogout = "{0}/api/logout".format(self.urlRouter)
        self.urlAccessControl = "{0}/api/firewall/accesscontrol".format(self.urlRouter)
        self.urlNetworkDevices = "{0}/api/devices".format(self.urlRouter)
        self.xsrfHeaderName = "X-XSRF-TOKEN"
        self.xsrfCookieName = "XSRF-TOKEN"
        self.setHeaders()
        """ Authenticate """
        if not self.isAuthenticated():
            self.authenticate()

    def __enter__(self):
        return self

    def setHeaders(self): 
        self.headers["Accept"] = "application/json,text/plain,*/*"
        self.headers["Referer"] = self.urlRouter 
        self.headers["User-Agent"] = "FrontierRouterApiApp"
        self.headers["Accept-Language"] = "en-US,en;q=0.8"
        self.headers["Accept-Encoding"] = "gzip,deflate,sdch"

    def getSha512PasswordHash(self):
        sha512 = hashlib.sha512()
        sha512.update(self.routerPassword)
        sha512.update(self.passwordSalt)
        return sha512.hexdigest()

    def isAuthenticated(self): 
        authenticated = False
        response = self.getResponse(self.urlLogin)
        if response.status_code == 401:
            authenticated = False
            jsonContent = json.loads(response.content)
            self.passwordSalt = jsonContent["passwordSalt"]
        elif response.status_code == 200:
            authenticated = True
        return authenticated

    def authenticate(self):
        authenticatedSuccessfully = False
        hashedPassword = self.getSha512PasswordHash()
        response = self.getResponse(self.urlLogin, "POST", json.dumps({"password":"{0}".format(hashedPassword)}))
        if response.status_code == 200:
            authenticatedSuccessfully = True
            for header in self.headers:
                if self.headers[header] == self.xsrfHeaderName:
                    del self.headers[header]
            for cookie in response.cookies:
                if cookie.name == self.xsrfCookieName:
                    self.headers[self.xsrfHeaderName] = cookie.value                
            if self.headers[self.xsrfHeaderName] == None:
                raise ValueError("XSRF token was not set.")
        return authenticatedSuccessfully

    def getResponse(self, url, method="GET", data={}):
        request = Request(method, url, headers=self.headers, data=data)
        prepped = self.session.prepare_request(request)
        response = self.session.send(prepped)
        return response

    def getResponseJson(self, url, method="GET", data={}):
        jsonData = {}
        response = self.getResponse(url, method, data)
        if response.status_code == 200:
            jsonData = json.loads(response.content)
        return jsonData

    def logOut(self):
        isLoggedOut = False
        self.headers["Connection"] = "close"
        response = self.getResponse(self.urlLogout)
        self.session.close()
        if response.status_code == 200:
            isLoggedOut = True
        return isLoggedOut

    def getAccessControl(self): 
        return self.getResponseJson(self.urlAccessControl)        
    
    def getNetworkDevices(self):
        return self.getResponseJson(self.urlNetworkDevices)

    def getAccessControlRuleStatus(self, ruleId):
        isActive = False
        accessControl = self.getAccessControl()
        for item in accessControl:
            if item["id"] == ruleId:
                isActive = item["active"]
        return isActive

    def toggleAccessControlRule(self, ruleId, activate):
        success = False
        response = self.getResponse("{0}/{1}".format(self.urlAccessControl, ruleId), "PUT", json.dumps({"active":activate}))
        if response.status_code == 200:
            success = True
        return success

    def __exit__(self, type, value, traceback):
        self.logOut()
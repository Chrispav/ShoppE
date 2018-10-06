
# using curl to interact with Amazon API
import pycurl
import io
import urllib
import json


# class that allows logging in through amazon account
class AmazonClient:
    accessToken = "test"

    def setAccessToken(self, token):
        self.accessToken = token

    def authenticate(self):
        b = io.BytesIO()

        # verify the access token
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://api.amazon.com/auth/o2/tokeninfo?access_token=" +
                 urllib.parse.quote_plus(self.accessToken))

        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.WRITEFUNCTION, b.write)

        c.perform()
        d = json.loads(b.getvalue())

        if d['error_index']:
            raise BaseException("Invalid Token")

        if d['aud'] != 'YOUR-CLIENT-ID':
            # access token is invalid
            raise BaseException("Invalid Token")

        # get the user profile
        b = io.StringIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://api.amazon.com.user.profile")
        c.setopt(pycurl.HTTPHEADER, ["Authorization: bearer " + self.accessToken])
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.WRITEFUNCTION, b.write)

        c.perform()
        d = json.loads(b.getvalue())

        print ("%s %s %s"%(d['name'], d['email'], d['user_id']))


x = AmazonClient()

x.authenticate()





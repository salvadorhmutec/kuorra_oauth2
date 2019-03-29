# Author        : Salvador Hernandez Mendoza
# Email         : salvadorhm@gmail.com
# Twitter       : @salvadorhm
# kuorra version: 0.7.2.3
# Created       : 10/Jul/2018

import web
import urls
import database


# Config database
db = database.db

# Activate ssl certificate
ssl = False

# secret_key for hmac technique
secret_key = "kuorra"

# Time session, after logout
expires = 5 # minutes

# Refres HTML rate
refresh = 60 # seconds

# Get urls
urls = urls.urls

# GOOGLE API OAUTH2

# Google API Token localhost
app_id = 'YOUR ID FOR LOCALHOST'
app_secret = 'YOUR SECRET KEY FOR LOCALHOST'

'''
# Google API Token salvadorhm.ddns.net
app_id = 'YOUR ID FOR CLOUD SERVER'
app_secret = 'YOUR SECRET KEY FOR CLOUD SERVER'
'''


# Global values
app = web.application(urls, globals())

if ssl is True:
    from web.wsgiserver import CherryPyWSGIServer
    CherryPyWSGIServer.ssl_certificate = "ssl/server.crt"
    CherryPyWSGIServer.ssl_private_key = "ssl/server.key"

if web.config.get('_session') is None:
    store = web.session.DBStore(db, 'sessions')
    session = web.session.Session(
        app,
        store,
        initializer={
        'login': 0,
        'privilege': -1,
        'user': 'anonymous',
        'picture': None,
        'expire': '0000-00-00 00:00:00',
        'loggedin': False,
        'count': 0
        }
        )
    web.config._session = session
else:
    session = web.config._session


class Count:
    def GET(self):
        session.count += 1
        return str(session.count)


def InternalError(): 
    raise web.seeother('/500')

def NotFound():
    raise web.seeother('/404')

if __name__ == "__main__":
    db.printing = False # hide db transactions
    web.config.debug = False # hide debug print
    web.config.db_printing = False # hide db transactions
    app.internalerror = InternalError # Web page for internal error
    app.notfound = NotFound # web page for page not found
    app.run()

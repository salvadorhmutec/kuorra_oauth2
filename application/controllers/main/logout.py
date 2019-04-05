import application.controllers.main.config as config
import app
import auth
import json
import web

class Logout:
    def __init__(self):
        pass

    def GET(self):
        app.session.loggedin = False # cierra la sesion en nuestro sistema
        app.session.user = 'anonymous' # se regresa a un usuario anonimo
        app.session.privilege = -1 #asignar privilegio solo para pagina de introduccion
        app.session.picture = None # se quita la url con la fotografia
        app.session.kill() # destruir la session de kuorra
        web.setcookie('_id', '', 0)#cierre de session en google 

        # raise config.web.seeother('https://accounts.google.com/Logout?&continue=http://www.kuorra.com/')
        raise config.web.seeother('https://accounts.google.com/Logout')
        # raise config.web.seeother('/')#redireccion al index


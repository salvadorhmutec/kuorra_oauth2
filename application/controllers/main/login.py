import application.controllers.main.config as config
import app
import hashlib
import web
import auth
import json
import datetime


# Google API Token creado en app.py
app_id = app.app_id
app_secret = app.app_secret

# Valores asignados de id_cliente proporcionado por el proveedor en este caso google
# En caso de trabajar con otros provedores como Facebook se cambiaran los valores
# En caso de trabajar con dos o mas provedores al mismo tiempo se tendran valores asiganados independientes por cada proveedor

auth.parameters['google']['app_id'] = app_id
auth.parameters['google']['app_secret'] = app_secret


class handler(auth.handler):
    def callback_uri(self, provider):
        return app.host_config % provider

    def on_signin(self, provider, profile):
        '''
        Una vez realizada la autenticacion por parte de Google
        se crear una cookie en el navegador con el "profile" perfil del
        usuario que inicio sesion.
        Los datos almacenados en la cookie permiten verificar si el usuario 
        que se autentico es una usuario valido en la base de datos del proyecto.
        '''
        user_id = '%s:%s' % (provider, profile['id'])
        web.setcookie('_id', user_id)
        web.setcookie('_profile', json.dumps(profile))
        raise web.seeother('/login')


class AuthPage(handler):
    def GET(self, provider):
        self.auth_init(provider)


class AuthCallbackPage(handler):
    def GET(self, provider):
        self.auth_callback(provider)


class Login:
    def __init__(self):
        pass

    def GET(self):
        if web.cookies().get('_id'):  # Esta cookie tiene el perfil del usuario devuelta por google
            # se almacena localmente el perfil del usuario desde la cookie
            profile = json.loads(web.cookies().get('_profile'))
            # email del usuario que se autentico con google
            user = profile['email']
            # url de la imagen del usuario que se autentico
            picture = profile['picture']
            '''
            El siguiente codigo verifica si el email del usuario que se autentico
            con google esta almacenado en la base de datos del proyecto.
            '''
            # user_authenticated, si el usuario existe en nuestro sistema regresa los datos el usuario
            # user_authenticated, no el usuario no existe en nuestro sistema regresa un valor None
            user_authenticated = config.model_users.validate_user(user)

            if user_authenticated:
                '''
                Se inicia sesion en el sistema con los datos dados por google y del proyecto
                '''
                app.session.loggedin = True  # sesion iniciada
                # email del usuario
                app.session.user = user_authenticated['user']
                # nivel del usuario
                app.session.privilege = user_authenticated['privilege']
                app.session.picture = picture  # fotografia del usuario google

                # Se establecen la hora y fecha actuales para el tiempo que estara abierta la sesion
                now = datetime.datetime.now()
                future = now + datetime.timedelta(minutes=app.expires)
                future_str = str(future).split('.')[0]
                app.session.expires = config.make_secure_val(future_str)

                # se obtiene la IP del usuario que esta iniciando sesion en el sistema
                ip = web.ctx['ip']

                # se guarda la ip y el usuario que inicio sesion
                config.model_logs.insert_logs(user_authenticated['user'], ip)

                # si el stuatus es 0 el usuario esta deshabilitado en el sistema
                if user_authenticated['status'] == 0:
                    message = user_authenticated['user'] + \
                        ": User account disabled!!!!"
                    app.session.loggedin = False  # se cierra la sesion
                    app.session.user = 'anonymous'  # se regresa a un usuario anonimo
                    app.session.privilege = -1  # asignar privilegio solo para pagina de introduccion
                    app.session.picture = None  # se quita la url con la fotografia
                    app.session.kill()  # destruir la session de kuorra
                    web.setcookie('_id', '', 0)  # cierre de session en google
                    # se renderiza nuevamente el login con el mensaje User account disabled
                    return config.render.login(message)
                else:
                    # si el usario esta habilitado lo reenvia la raiz del sistema
                    raise config.web.seeother('/')

            if user_authenticated is None:  # usuario no registrado en nuestro sistema
                message = user + ": User not found"  # establece el mensaje User not found
                app.session.loggedin = False  # cierra la sesion en nuestro sistema
                app.session.user = 'anonymous'  # se regresa a un usuario anonimo
                app.session.privilege = -1  # asignar privilegio solo para pagina de introduccion
                app.session.picture = None  # se quita la url con la fotografia
                app.session.kill()  # destruir la session de kuorra
                web.setcookie('_id', '', 0)  # cierre de session en google

                print message
                return config.render.login(message)
        else:  # si no inicio session correctamente con google vuelve a solicitar que la inicie
            # pagina para iniciar sesion con google
            raise web.seeother('/auth/google')

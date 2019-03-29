import web

db_host = 'localhost'
db_name = 'kuorra_login_google'
db_user = 'kuorra_google'
db_pw = 'kuOrra.2018'
db_port = 3308

db = web.database(
    dbn = 'mysql',
    host = db_host,
    db = db_name,
    user = db_user,
    pw = db_pw,
    port = db_port
    )
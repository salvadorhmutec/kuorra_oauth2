# Kuorra login with Google API oauth 2.0

## Introduction

Kuorra is a Web.py Microframework Frontend, use kuorra to create a MVC skeleton for work with Web.py, MySQL and Heroku App.


## GOOGLE API OAUTH2.0

1. For use the google API oauth2.0 first is needed create a proyect in google developer console at next link

    - [Google Developer Console](https://console.developers.google.com)

2. Select the proyect created and create credencials in the next link

    - [Google Developer Credentials](https://console.developers.google.com/apis/credentials)

3. Create  ID client for OAuth

    - Choose Web Application.

    - Give a name to the Application.

    - URI redirection, choose:
        - For work in local:
            - http://localhost:8080/auth/google/callback
        - For work in the web:
            - http://yourwebserver.com:8080/auth/google/callback
            - or
            - http://proyect.herokuapp.com/auth/google/callback

    - GET tokens for use in **app.py**
        - app_id 
        - app_secret

4. Config remote or local use

    - variable remote in app.py choose localhost or remote host

5. Check the file login.py

    - This file is used for validate a user from proyect database, after google authenticated the user account.
    - This file can be used for:
        1. Validate user for the system.
        2. Register a new user
# -*- coding: utf-8 -*-

from bottle import Bottle, run, error, template, static_file, request, redirect
from google.appengine.ext import ndb
from google.appengine.api import users

app = Bottle()
g_name = 'SkyWind'

base_key = ndb.Key('Apps', 'KF_Apps')

class Applic(ndb.Model):
    title = ndb.StringProperty(indexed=True)
    content = ndb.TextProperty(indexed=False, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    user = users.get_current_user()
    if user:
        return template('index', name=g_name, user = user.nickname(), lo = users.create_logout_url('/'), opt = 'Выход')
    else:
        return template('index', name=g_name, lo = users.create_login_url('/'), opt = 'Войти')
        

    

@app.route('/add')
def addapp():
    user = users.get_current_user()
    if user:
        return template('add', name=g_name, lo = users.create_logout_url('/'), opt = 'Выход')
    else:
        redirect('/')
    
	
@app.route('/add', method='POST')
def save():
    user = users.get_current_user()
    if user:
        new_app = Applic(parent=base_key)
        new_app.content = request.forms.get('content')
        new_app.title = request.forms.get('title')   
        new_app.put()
        redirect('/')
    else:
        redirect('/')

@app.route('/applist')
def app_list():
    user = users.get_current_user()
    if user:
        appls_query = Applic.query(ancestor = base_key).order(-Applic.date)
        appls = appls_query.fetch()
        output = template('applist', appls=appls, name=g_name, lo = users.create_logout_url('/'), opt = 'Выход')
        return output
    else:
        redirect('/')

@app.route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)
	
@app.route('/new/<pagename>')            # matches /wiki/Learning_Python
def show_page(pagename):
    return template('This {{name}} page.', name=pagename)
	
@app.route('/temp')
def greet(name='Tempo'):
    return template('temp1', name=name)

@app.route('/error')
def error_page():  
    return "Error!"

@app.error(403)
def Error403(code):
    return 'Get your codes right dude, you caused some error!'

app.error(404)
def Error404(code):
    return 'Stop cowboy, what are you trying to find?'

run(app=app, server='gae')
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import json
from bottle import Bottle, run, error, template, static_file, request, redirect, route, response
from google.appengine.ext import ndb
from google.appengine.api import users


app = Bottle()
g_name = 'SkyWind'

base_key = ndb.Key('Applic', 'KF_Apps')
admin_base = ndb.Key('Admins', 'admin_base')
user_base = ndb.Key('Users', 'user_base')

class Applic(ndb.Model):
    username = ndb.StringProperty(indexed=False, required=True)
    user = ndb.StringProperty(indexed=True, required=True)
    title = ndb.StringProperty(indexed=True)
    content = ndb.TextProperty(indexed=False, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Admins(ndb.Model):
    admin_nick = ndb.StringProperty(indexed=False, required=True)
    admin_id = ndb.StringProperty(indexed=True, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    ref_nick = ndb.StringProperty(indexed=False, required=True)
    
class Users(ndb.Model):
    id = ndb.StringProperty(indexed=False, required=True)  #  local App System ID
    gid = ndb.StringProperty(indexed=False, required=False) # google ID
    vkid = ndb.StringProperty(indexed=False, required=False)  # Vkontakte user ID
    login_type = ndb.IntegerProperty(indexed=False, required=True) # login type: 1 - google, 2 - vkontakte
    
    
    
def is_local_admin():
    """Cheking for admin rights for current user. Uses ndb"""
    admins_query = Admins.query(ancestor = admin_base)
    admins = admins_query.fetch()
    user = users.get_current_user()
    if user: 
        userid = user.user_id()
        for each_admin in admins:
            if each_admin.admin_id == userid:
                return True
        return False        
    return False

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    """Handler for index page"""
    user = users.get_current_user()
    if user:
        return template('index', name=g_name, user = user.nickname(), log_in_out = users.create_logout_url('/'), opt = 'Выход')
    else:
        return template('index', name=g_name, log_in_out = users.create_login_url('/'), opt = 'Войти')
        

@app.route('/add')
def addapp():
    """Handler for add new application page"""
    user = users.get_current_user()
    if user:
        return template('add', name=g_name, log_in_out = users.create_logout_url('/'), opt = 'Выход', user = user.nickname())
    else:
        redirect('/')
    
	
@app.route('/add', method='POST')
def save():
    """Handler for add new application page POST method"""
    user = users.get_current_user()
    if user:
        new_app = Applic(parent=base_key)
        new_app.user = user.user_id()
        new_app.username = user.nickname()
        new_app.content = request.forms.get('content')
        new_app.title = request.forms.get('title')   
        new_app.put()
        redirect('/')
    else:
        redirect('/')

@app.route('/applist')
def app_list():
    """Handler for application list page"""
    user = users.get_current_user()
    if user:
        if users.is_current_user_admin() or is_local_admin():
            appls_query = Applic.query(ancestor = base_key).order(-Applic.date)
            appls = appls_query.fetch()
            output = template('applist', appls=appls, name=g_name, log_in_out = users.create_logout_url('/'), opt = 'Выход', user = user.nickname())
            return output
        else:
            userid = user.user_id()
            #return userid
            appls_query = Applic.query(Applic.user==userid).order(-Applic.date)
            appls = appls_query.fetch()
            output = template('applist', appls=appls, name=g_name, log_in_out = users.create_logout_url('/'), opt = 'Выход', user = user.nickname())
            return output
    else:
        redirect('/')

@app.route('/admin')
def admin_con():
    """Handler for admin console (now is very ugly)"""
    user = users.get_current_user()
    if user:
        if users.is_current_user_admin() or is_local_admin():
            admins_query = Admins.query(ancestor = admin_base).order(-Admins.date)
            admins = admins_query.fetch()
            output = template('admin', name=g_name, log_in_out = users.create_logout_url('/'), opt = 'Выход', user = user.nickname(), admins = admins)
            return output
        else:
            redirect('/')
    else:
        redirect('/')
        
@app.route('/admin', method='POST')
def save_admin():
    """Handler for add admin in admin console. method POST"""
    user = users.get_current_user()
    if user:
        if users.is_current_user_admin() or is_local_admin():
            added_admin_mail = request.forms.get('mail')
            added_admin = users.User(added_admin_mail)
            if added_admin:
                #return added_admin.user_id()
                #output = added_admin.nickname()+ ' ' + added_admin.user_id()
                #return output
                new_admin = Admins(parent=admin_base)
                new_admin.ref_nick = user.nickname()
                new_admin.admin_nick = added_admin.nickname()
                new_admin.admin_id = 'no id'#added_admin.user_id()
                new_admin.put()
                redirect('/admin')
                
            else:
                #return "Не получилось"
                output = template('admin', name=g_name, log_in_out = users.create_logout_url('/'), opt = 'Выход', user = user.nickname(), admins = admins, error="Неверный email")
                return output
        else:
            redirect('/')
    else:
        redirect('/')

@app.route('/isadmin')
def is_admin():
    """Handler for admin right cheking page"""
    user = users.get_current_user()
    if user:
        if users.is_current_user_admin() or is_local_admin():
            return 'Yes, you are admin'
        else:
            return "No, you don't admin"
    else:
        return "You not logged in"

@app.route('/vklogin')
def vk_login():
    """Handler for login with Vkontakte page"""
    return template('vklogin')

    
vk_client_id = '4712400'
vk_client_secret = 'oZCpBbYCgK1EIMlMFiHi'
vk_redirect_url = 'http://localhost:8080/vkloginres'
vk_token_url = "https://oauth.vk.com/access_token"
vk_user_get_url = "https://api.vk.com/method/users.get"
    
@app.route('/vkloginres')
def vk_login_response_handler():
    """Vkontakte login handler"""
    code = request.query.code
    if code:
        data = {'client_id':vk_client_id,'client_secret':vk_client_secret,'code':code}
        data_url = urllib.urlencode(data)
        vk_token_request_data = vk_token_url + '?' + data_url + '&' + 'redirect_uri' + '=' + vk_redirect_url
        
        try:
            vk_answer = urllib2.urlopen(vk_token_request_data)
            
        except urllib2.HTTPError as HTTP_err:
            if (str(sys.exc_info()[1].code) == '401'):
                return "Ошибка авторизации <a href='https://oauth.vk.com/authorize?client_id=4712400&redirect_uri=http://localhost:8080/vkloginres&response_type=code'>Попробовать еще</a>"
            else:
                return str(HTTP_err) +' '+ str(sys.exc_info()[1].code)
        
        vk_answer_decoded = json.load(vk_answer) 

        vk_token = vk_answer_decoded['access_token']
        vk_token_expires = vk_answer_decoded['expires_in']
        vk_userid = vk_answer_decoded['user_id']
        vk_data_request = vk_user_get_url + '?' + urllib.urlencode({'uids': vk_userid, 'fields': 'uid,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo_max_orig', 'access_token': vk_token})
        
        try:
            vk_answer = urllib2.urlopen(vk_data_request)
        except urllib2.HTTPError as HTTP_err:
            return str(HTTP_err) +' '+ str(sys.exc_info()[1].code)
            
        vk_answer_decoded = json.load(vk_answer)
        #return vk_answer_decoded["response"][0]['first_name']
        vk_userid = vk_answer_decoded["response"][0]['uid']
        vk_firstname = vk_answer_decoded["response"][0]['first_name']
        vk_lastname = vk_answer_decoded["response"][0]['last_name']
        vk_nickname = vk_answer_decoded["response"][0]['nickname']
        
        if vk_answer_decoded["response"][0]['sex'] == 2:
            vk_gender = "Мужской"
        elif vk_answer_decoded["response"][0]['sex'] == 1:
            vk_gender = "Женский"
        else:
            vk_gender = "Не определен"

        vk_photo = vk_answer_decoded["response"][0]['photo_max_orig']
        
                

        output = template("User ID: {{userid}}<br />Имя: {{name}}<br />Фамилия: {{surname}}<br />Ник: {{nick}}<br />Пол: {{gender}}<br /><img src={{photo}} alt='Фото'>", userid = vk_userid, name = vk_firstname, surname = vk_lastname, nick = vk_nickname, gender = vk_gender, photo = vk_photo)
        
        return output
        
        
    else:
        return request.query.error
        
@app.route('/vkloginapi')
def vk_login_api():

    return template("apilogin", id = vk_client_id)
    
@app.route('/getcookie')
def get_cookie():
    cook = request.get_cookie("vk_app_"+vk_client_id)
    return str(cook)
    
@app.route('/setcookie')
def set_cookie():
    count = int( request.get_cookie('counter', '0') )
    count += 1
    response.set_cookie('counter', str(count))
    return 'You visited this page %d times' % count

        
@app.route('/test')
def test_query():
    answer = urllib2.urlopen("http://oauth.vk.com/access_token")
    return answer.read()
        
'''@app.route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)
	
@app.route('/new/<pagename>')
def show_page(pagename):
    return template('This {{name}} page.', name=pagename)
	
@app.route('/temp')
def greet(name='Tempo'):
    return template('temp1', name=name)
    
@app.route('/id')
def id():
    user = users.get_current_user()
    return user.user_id()'''

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
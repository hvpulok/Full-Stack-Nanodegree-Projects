# This file defines server side definitions
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Subject, Course, User

import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

#Connect to Database and create database session
engine = create_engine('sqlite:///course_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['access_token'] = access_token
    login_session['provider'] = 'google'

    # see if user already exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output



# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    # return "Google"
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'    
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
        
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"




#Show all subjects in catalog
@app.route('/')
def index():
    if 'user_id' in login_session:
        user_id = login_session['user_id']
    else:
        user_id = ""
    allSubjects = session.query(Subject).order_by(asc(Subject.name))
    allcourses = session.query(Course).order_by(desc(Course.id))
    return render_template('index.html', courses = allcourses, subjects = allSubjects, user_id=user_id)

@app.route('/subjects/')
def showSubjects():
    subjects = session.query(Subject).order_by(asc(Subject.name))
    return render_template('subjects.html', subjects = subjects)
    # return "Welcome"


#Create a new subject
@app.route('/subjects/new/', methods=['GET','POST'])
def newSubject():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newSubject = Subject(name = request.form['name'],
                                    user_id = login_session['user_id'],
                                    user_name = login_session['username'])
        session.add(newSubject)
        flash('New Subject "%s" Successfully Created' % newSubject.name)
        session.commit()
        return redirect(url_for('showSubjects'))
    else:
        return render_template('newSubject.html')


#Edit a subject
@app.route('/subjects/<int:subject_id>/edit/', methods = ['GET', 'POST'])
def editSubject(subject_id):
    if 'username' not in login_session:
        return redirect('/login')
    editSubject = session.query(Subject).filter_by(id = subject_id).one()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        if (user_id != editSubject.user_id) : 
            return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editSubject.name = request.form['name']
            session.add(editSubject)
            session.commit() 
            flash('Subject Successfully Edited %s' % editSubject.name)
            return redirect(url_for('showSubjects'))
    else:
        return render_template('editSubject.html', subject = editSubject)


#Delete a subject
@app.route('/subjects/<int:subject_id>/delete/', methods = ['GET', 'POST'])
def deleteSubject(subject_id):
    if 'username' not in login_session:
        return redirect('/login')
    subjectToDelete = session.query(Subject).filter_by(id = subject_id).one()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        if (user_id != subjectToDelete.user_id) : 
            return redirect('/login')
    if request.method == 'POST':
        session.delete(subjectToDelete)
        flash('%s Successfully Deleted' % subjectToDelete.name)
        session.commit()
        return redirect(url_for('showSubjects'))
    else:
        return render_template('deleteSubject.html',subject = subjectToDelete)


#Show selected subject's all course catalog
# @app.route('/subjects/<int:subject_id>/')
@app.route('/subjects/<int:subject_id>/course/')
def showCourse(subject_id):
    if 'user_id' in login_session:
        user_id = login_session['user_id']
    else:
        user_id = ""
    allSubjects = session.query(Subject).order_by(asc(Subject.name))
    subject = session.query(Subject).filter_by(id = subject_id).one()
    courses = session.query(Course).filter_by(subject_id = subject_id).all()
    return render_template('courses.html', courses = courses, subject = subject, allSubjects = allSubjects, user_id=user_id)

#Show selected course's details
@app.route('/subjects/<int:subject_id>/course/<int:course_id>')
def courseDetails(subject_id, course_id):
    if 'user_id' in login_session:
        user_id = login_session['user_id']
    else:
        user_id = ""
    allSubjects = session.query(Subject).order_by(asc(Subject.name))
    allCourses = session.query(Course).filter_by(subject_id = subject_id).all()
    selectedCourse = session.query(Course).filter_by(id = course_id).one()
    subject = session.query(Subject).filter_by(id = subject_id).one()
    return render_template('courseDetails.html', subject = subject, selectedCourse = selectedCourse,courses = allCourses, allSubjects = allSubjects, user_id=user_id)


#Add new course
@app.route('/subjects/<int:subject_id>/course/new/', methods=['GET','POST'])
def newCourse(subject_id):
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        author_name = login_session['username']
    else:
        return redirect('/login')
    allSubjects = session.query(Subject).order_by(asc(Subject.name))
    allCourses = session.query(Course).filter_by(subject_id = subject_id).all()
    subject = session.query(Subject).filter_by(id = subject_id).one()

    if request.method == 'POST':
        newCourse = Course(name = request.form['name'], 
                            description = request.form['description'], 
                            price = request.form['price'], 
                            subject_id = subject_id, 
                            author_name = author_name,
                            user_id = user_id)
        session.add(newCourse)
        session.commit()
        flash('New Course "%s" Successfully Created' % (newCourse.name))
        return redirect(url_for('showCourse', subject_id = subject_id))        
    else:
        return render_template('newCourse.html', subject = subject, courses = allCourses, allSubjects = allSubjects, user_id=user_id)


#edit selected course's details
@app.route('/subjects/<int:subject_id>/course/<int:course_id>/edit', methods=['GET','POST'])
def editCourse(subject_id, course_id):
    editedCourse = session.query(Course).filter_by(id = course_id).one()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        if (user_id != editedCourse.user_id) : 
            return redirect('/login')
    else:
        return redirect('/login')
    allSubjects = session.query(Subject).order_by(asc(Subject.name))
    allCourses = session.query(Course).filter_by(subject_id = subject_id).all()
    subject = session.query(Subject).filter_by(id = subject_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedCourse.name = request.form['name']
        if request.form['description']:
            editedCourse.description = request.form['description']
        if request.form['price']:
            editedCourse.price = request.form['price']
        session.add(editedCourse)
        session.commit() 
        flash('Selected Course Successfully Updated')
        return redirect(url_for('courseDetails', subject_id = subject_id, course_id=course_id))
    else:
        return render_template('editCourse.html', subject = subject, selectedCourse = editedCourse,courses = allCourses, allSubjects = allSubjects, user_id=user_id)

    
#Delete selected Course
@app.route('/subjects/<int:subject_id>/course/<int:course_id>/delete', methods = ['GET','POST'])
def deleteCourse(subject_id, course_id):
    deleteCourse = session.query(Course).filter_by(id = course_id).one()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        if (user_id != deleteCourse.user_id) : 
            return redirect('/login')
    else:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(deleteCourse)
        session.commit()
        flash('Selected Course Successfully Deleted')
        return redirect(url_for('showCourse', subject_id = subject_id))
    else:
        return render_template('deleteCourse.html', subject_id = subject_id, deleteCourse = deleteCourse)



# Disconnect based on provider
@app.route('/logout')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            value = gdisconnect()
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['user_id']
            del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showSubjects'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showSubjects'))

# Server host and port definition starts here
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
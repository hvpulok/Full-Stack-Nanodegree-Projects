# This file defines server side definitions
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Subject, Course, User

import random, string

app = Flask(__name__)

#Connect to Database and create database session
engine = create_engine('sqlite:///course_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Show all subjects in catalog
@app.route('/')
@app.route('/subjects/')
def showSubjects():
    return "Welcome"



# Server host and port definition starts here
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
# This file populates database with seed data

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Subject, Course, User

engine = create_engine('sqlite:///course_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# =========================================================


def deleteAllUsers():
    """ Delete all existing users """
    result = session.query(User).all()
    for item in result:
        session.delete(item)
    
    session.commit()

def deleteDummySubjects():
    """ Delete all existing subjects """
    result = session.query(Subject).all()
    for item in result:
        session.delete(item)

def deleteDummyCourses():
    """ Delete all existing courses """
    result = session.query(Course).all()
    for item in result:
        session.delete(item)


def createDummyUsers():
    """Create dummy user"""
    User1 = User(   name="Admin", 
                    email="admin@random.com", 
                    picture='http://lorempixel.com/200/200/people/')
    User2 = User(   name="Mike", 
                    email="mike@random.com", 
                    picture='http://lorempixel.com/200/200/people/')
    User3 = User(   name="Sara", 
                    email="sara@random.com", 
                    picture='http://lorempixel.com/200/200/people/')

    session.add(User1)
    session.add(User2)
    session.add(User3)
    session.commit()


def createDummySubjects():
    """Create dummy Subject"""
    sub1 = Subject( user_id= 1, name="Web Development")
    sub2 = Subject( user_id= 1, name="Mobile App Development")
    sub3 = Subject( user_id= 2, name="Game Development")

    session.add(sub1)
    session.add(sub2)
    session.add(sub3)
    session.commit()


def createDummyCourses():
    """Create dummy Courses"""
    course1 = Course( user_id= 3, subject_id=1, name="Web Developer Bootcamp", 
                description= "The only course you need to learn web development - HTML, CSS, JS, Python, and More!",
                price = "$50")
    course2 = Course( user_id= 2, subject_id=1,  name="Accelerated Java Script Training", 
                description= " Know how to code in Java script",
                price = "$25")
    course3 = Course( user_id= 1, subject_id=1,  name="HTML5 Training", 
                description= "HTML5 Programming explained in detail",
                price = "$20")


    session.add(course1)
    session.add(course2)
    session.add(course3)
    session.commit()


def showAllUsers():
    """Query all of the users and return the results in ascending alphabetical order"""
    result = session.query(User).order_by(User.name.asc()).all()

    for item in result:
        print item.id, item.name

def showAllSubjects():
    """Query all of the subjects and return the results in ascending id order"""
    result = session.query(Subject).order_by(Subject.id.asc()).all()

    for item in result:
        print item.id, item.name, item.user_id   

def showAllCourses():
    """Query all of the course and return the results in ascending id order"""
    result = session.query(Course).order_by(Course.id.asc()).all()

    for item in result:
        print item.id, item.name, item.price, item.subject_id, item.user_id      

print "========================================================="
print "Databased seeding started"
print "========================================================="

deleteDummyCourses()
deleteDummySubjects()
deleteAllUsers()


createDummyUsers()
createDummySubjects()
createDummyCourses()

print "----User-ID, Username---------"
showAllUsers()

print "----SubjectID, Subject Name, Author ID---------"
showAllSubjects()

print "----CourseID, Course Name, Course Price, Subject_id, Author ID---------"
showAllCourses()

print "========================================================="
print "Databased seeded successfully with dummy data"
print "========================================================="
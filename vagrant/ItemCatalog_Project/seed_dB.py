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
                description= "Lorem ipsum dolor sit amet, nunc erat voluptatem dapibus maecenas leo. Fusce placerat urna enim odio, ante leo ligula cras nam, mauris dolor gravida libero, proin aliquam velit duis gravida viverra ipsum, adipiscing habitant. Scelerisque nulla mollis nulla, fermentum non vel amet tellus mi, id posuere, a ipsum a metus amet leo, risus mi ullamcorper at facilisis etiam aliquam. Luctus ligula ligula metus. Ut pretium turpis donec vestibulum nulla, tellus arcu auctor morbi vitae, vitae ut ornare porttitor ut proin, urna mi elit sed dui euismod, enim sed vestibulum blandit. A sed dolor, tellus felis turpis, viverra voluptas commodo, malesuada vel mauris auctor, massa suspendisse fermentum.",
                price = "$50")
    course2 = Course( user_id= 2, subject_id=1,  name="Accelerated Java Script Training", 
                description= "Fermentum accumsan pede maecenas at vivamus vitae, varius esse nascetur blandit, aliquam montes dictum tristique odio, pellentesque sed fusce magna nulla, sodales est id libero. Lobortis in tellus dapibus massa ac, nisl luctus at nam nec eu, morbi cras porta vestibulum nulla posuere, aliquam malesuada. Mauris vel reiciendis tempus consectetuer egestas tellus, tempus faucibus sodales, tellus in elementum auctor habitasse, odio mauris, dis et at diam urna purus nunc. Id bibendum fermentum, et leo feugiat pellentesque metus ultricies, fringilla adipiscing, habitasse fringilla. In consectetuer aliquip erat parturient orci, integer pede risus quam quis porta. Scelerisque pharetra massa habitant sodales elementum, ornare nostra adipiscing.",
                price = "$25")
    course3 = Course( user_id= 1, subject_id=1,  name="HTML5 Training", 
                description= "Elit senectus consectetuer gravida ultricies sit magnis, nunc sed tincidunt, tempus amet montes sed aliquam pellentesque placerat. Eros aenean vel id turpis, feugiat lacus, lectus eget et. Dolor bibendum vitae augue placerat, tincidunt vel nibh pulvinar omnis feugiat et, adipiscing sed primis urna leo ad, ligula suspendisse vel. Hymenaeos ac vel turpis, luctus egestas sagittis molestie risus quis nunc, feugiat ornare fusce diam ut, et vitae fringilla iaculis quis. Ut sed nulla, vitae wisi ac aliquam vestibulum mauris, fusce malesuada dictum sit ultricies convallis rutrum. Sapien blandit massa sapien ligula a nulla, elementum ipsum volutpat id, sed diam erat, egestas eum sed dictumst tempor, tortor porttitor adipiscing ad ipsum temporibus.",
                price = "$20")
    course4 = Course( user_id= 3, subject_id=2, name="Mobile App Developer Bootcamp", 
                description= "Lorem ipsum dolor sit amet, nunc erat voluptatem dapibus maecenas leo. Fusce placerat urna enim odio, ante leo ligula cras nam, mauris dolor gravida libero, proin aliquam velit duis gravida viverra ipsum, adipiscing habitant. Scelerisque nulla mollis nulla, fermentum non vel amet tellus mi, id posuere, a ipsum a metus amet leo, risus mi ullamcorper at facilisis etiam aliquam. Luctus ligula ligula metus. Ut pretium turpis donec vestibulum nulla, tellus arcu auctor morbi vitae, vitae ut ornare porttitor ut proin, urna mi elit sed dui euismod, enim sed vestibulum blandit. A sed dolor, tellus felis turpis, viverra voluptas commodo, malesuada vel mauris auctor, massa suspendisse fermentum.",
                price = "$50")
    course5 = Course( user_id= 2, subject_id=2,  name="Learn iOS Developement", 
                description= "Fermentum accumsan pede maecenas at vivamus vitae, varius esse nascetur blandit, aliquam montes dictum tristique odio, pellentesque sed fusce magna nulla, sodales est id libero. Lobortis in tellus dapibus massa ac, nisl luctus at nam nec eu, morbi cras porta vestibulum nulla posuere, aliquam malesuada. Mauris vel reiciendis tempus consectetuer egestas tellus, tempus faucibus sodales, tellus in elementum auctor habitasse, odio mauris, dis et at diam urna purus nunc. Id bibendum fermentum, et leo feugiat pellentesque metus ultricies, fringilla adipiscing, habitasse fringilla. In consectetuer aliquip erat parturient orci, integer pede risus quam quis porta. Scelerisque pharetra massa habitant sodales elementum, ornare nostra adipiscing.",
                price = "$25")
    course6 = Course( user_id= 1, subject_id=2,  name="Mastering Android Developement", 
                description= "Elit senectus consectetuer gravida ultricies sit magnis, nunc sed tincidunt, tempus amet montes sed aliquam pellentesque placerat. Eros aenean vel id turpis, feugiat lacus, lectus eget et. Dolor bibendum vitae augue placerat, tincidunt vel nibh pulvinar omnis feugiat et, adipiscing sed primis urna leo ad, ligula suspendisse vel. Hymenaeos ac vel turpis, luctus egestas sagittis molestie risus quis nunc, feugiat ornare fusce diam ut, et vitae fringilla iaculis quis. Ut sed nulla, vitae wisi ac aliquam vestibulum mauris, fusce malesuada dictum sit ultricies convallis rutrum. Sapien blandit massa sapien ligula a nulla, elementum ipsum volutpat id, sed diam erat, egestas eum sed dictumst tempor, tortor porttitor adipiscing ad ipsum temporibus.",
                price = "$20")
    course7 = Course( user_id= 3, subject_id=3, name="Game Developer Bootcamp", 
                description= "Lorem ipsum dolor sit amet, nunc erat voluptatem dapibus maecenas leo. Fusce placerat urna enim odio, ante leo ligula cras nam, mauris dolor gravida libero, proin aliquam velit duis gravida viverra ipsum, adipiscing habitant. Scelerisque nulla mollis nulla, fermentum non vel amet tellus mi, id posuere, a ipsum a metus amet leo, risus mi ullamcorper at facilisis etiam aliquam. Luctus ligula ligula metus. Ut pretium turpis donec vestibulum nulla, tellus arcu auctor morbi vitae, vitae ut ornare porttitor ut proin, urna mi elit sed dui euismod, enim sed vestibulum blandit. A sed dolor, tellus felis turpis, viverra voluptas commodo, malesuada vel mauris auctor, massa suspendisse fermentum.",
                price = "$50")
    course8 = Course( user_id= 2, subject_id=3,  name="Learn by building a working Game", 
                description= "Fermentum accumsan pede maecenas at vivamus vitae, varius esse nascetur blandit, aliquam montes dictum tristique odio, pellentesque sed fusce magna nulla, sodales est id libero. Lobortis in tellus dapibus massa ac, nisl luctus at nam nec eu, morbi cras porta vestibulum nulla posuere, aliquam malesuada. Mauris vel reiciendis tempus consectetuer egestas tellus, tempus faucibus sodales, tellus in elementum auctor habitasse, odio mauris, dis et at diam urna purus nunc. Id bibendum fermentum, et leo feugiat pellentesque metus ultricies, fringilla adipiscing, habitasse fringilla. In consectetuer aliquip erat parturient orci, integer pede risus quam quis porta. Scelerisque pharetra massa habitant sodales elementum, ornare nostra adipiscing.",
                price = "$25")
    course9 = Course( user_id= 1, subject_id=3,  name="Become A Game Developer", 
                description= "Elit senectus consectetuer gravida ultricies sit magnis, nunc sed tincidunt, tempus amet montes sed aliquam pellentesque placerat. Eros aenean vel id turpis, feugiat lacus, lectus eget et. Dolor bibendum vitae augue placerat, tincidunt vel nibh pulvinar omnis feugiat et, adipiscing sed primis urna leo ad, ligula suspendisse vel. Hymenaeos ac vel turpis, luctus egestas sagittis molestie risus quis nunc, feugiat ornare fusce diam ut, et vitae fringilla iaculis quis. Ut sed nulla, vitae wisi ac aliquam vestibulum mauris, fusce malesuada dictum sit ultricies convallis rutrum. Sapien blandit massa sapien ligula a nulla, elementum ipsum volutpat id, sed diam erat, egestas eum sed dictumst tempor, tortor porttitor adipiscing ad ipsum temporibus.",
                price = "$20")



    session.add(course1)
    session.add(course2)
    session.add(course3)
    session.add(course4)
    session.add(course5)
    session.add(course6)
    session.add(course7)
    session.add(course8)
    session.add(course9)
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
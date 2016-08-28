# This file setup ecourse catalog database definitions and schemas

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    """ This clas defines User dB schema """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Subject(Base):
    """ This clas defines subjects dB schema """
    __tablename__ = 'subject'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user_name = Column(Integer, ForeignKey('user.name'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return subjects object data in easily serializeable format"""
       return {
            'id'                    : self.id,
            'name'                  : self.name,
            'user_id'               : self.user_id,           
            'user_name'             : self.user_name,           
       }


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(10000))
    price = Column(String(8))
    subject_id = Column(Integer,ForeignKey('subject.id'))
    subject = relationship(subject)
    author_id = Column(Integer, ForeignKey('user.id'))
    author_name = Column(Integer, ForeignKey('user.name'))
    user = relationship(User)


    @property
    def serialize(self):
       """Return Course object data in easily serializeable format"""
       return {
            'id'                    : self.id,
            'name'                  : self.name,
            'description'           : self.description,
            'price'                 : self.price,
            'subject'               : self.subject,
            'author_id'             : self.author_id,    
            'author_name'           : self.author_name,    
       }

# definition to create database engine
engine = create_engine('sqlite:///course_catalog.db')
Base.metadata.create_all(engine)
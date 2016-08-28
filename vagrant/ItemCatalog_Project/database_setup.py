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

class subjects(Base):
    """ This clas defines subjects dB schema """
    __tablename__ = 'subjects'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return subjects object data in easily serializeable format"""
       return {
            'name'         : self.name,
            'id'           : self.id,
            'user_id'      : self.user_id,           
       }

# definition to create database engine
engine = create_engine('sqlite:///course_catalog.db')
Base.metadata.create_all(engine)
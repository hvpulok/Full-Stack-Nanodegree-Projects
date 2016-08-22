import sys

from sqlalchemy import column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()





######## insert at the end of file ########

engine = create_engine('sqlite://restaurantmenu.db')
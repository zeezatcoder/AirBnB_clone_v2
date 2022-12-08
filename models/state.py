#!/usr/bin/python3
""" State Module """
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State Schema Definition """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",
                          backref="state", cascade="all, delete,delete-orphan")

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """ returns cities related to state """
            from models import storage
            arr_cities = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    arr_cities.append(city)
            return arr_cities

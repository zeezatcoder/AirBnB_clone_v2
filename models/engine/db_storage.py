#!/usr/bin/python3
"""Database Storage module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """SQL database storage creations"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and connect to database"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)

        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of objects"""
        obj = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for item in query:
                key = "{}.{}".format(type(item).__name__, item.id)
                obj[key] = item
        else:
            db_cls = [State, City, User, Place, Review, Amenity]
            for clss in db_cls:
                query = self.__session.query(clss)
                for item in query:
                    key = "{}.{}".format(type(item).__name__, item.id)
                    obj[key] = item
        return (obj)

    def new(self, obj):
        """add new dabase record to session"""
        self.__session.add(obj)

    def save(self):
        """commit current session changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete current session object from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload sessions from the database"""
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """ close a session"""
        self.__session.close()

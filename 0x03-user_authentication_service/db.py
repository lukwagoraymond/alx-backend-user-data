#!/usr/bin/env python3
"""Module contains DB Class Definitions"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """creates a User Object & saves it to a DB"""
        try:
            user_obj = User(email=email, hashed_password=hashed_password)
            self._session.add(user_obj)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user_obj = None
        return user_obj

    def find_user_by(self, **kwargs) -> User:
        """method takes in arbitrary keyword arguments
        and returns the 1st row found in the user tables"""
        for key, val in kwargs.items():
            if hasattr(User, key):
                continue
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates selected instance in DB with new
        attributes"""
        result = self.find_user_by(id=user_id)
        if result:
            for key, val in kwargs.items():
                if hasattr(User, key):
                    setattr(result, key, val)
                else:
                    raise ValueError
            self._session.commit()
        return None

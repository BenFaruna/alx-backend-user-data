#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
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
        self._engine = create_engine("sqlite:///a.db",
                                     connect_args={'check_same_thread': False})
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None
        self._session

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str = None, hashed_password: str = None) -> User:
        """method save the user to the database"""
        if email is None or hashed_password is None:
            return
        user = User(email=email, hashed_password=hashed_password)
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users table
        filtered by the input arguments"""
        for key in kwargs:
            if key not in User.__table__.columns:
                raise InvalidRequestError

        user = self.__session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """will update the user attributes as passed in the method arguments"""
        user = self.find_user_by(id=user_id)
        for key in kwargs:
            if key not in User.__table__.columns:
                raise ValueError

            setattr(user, key, kwargs[key])
        self.__session.commit()

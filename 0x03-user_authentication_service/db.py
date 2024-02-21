#!/usr/bin/env python3

"""
Database Module
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    SqlAlchemy Database Class
    """

    def __init__(self) -> None:
        """
        Init a new db instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized Session obj
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add user to database
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find user based on filters
        """
        filters, values = [], []
        for k, v in kwargs.items():
            if hasattr(User, k):
                filters.append(getattr(User, k))
                values.append(v)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*filters).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user based on id
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        updated_value = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                updated_value[getattr(User, k)] = v
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            updated_value, synchronize_session=False
        )
        self._session.commit()

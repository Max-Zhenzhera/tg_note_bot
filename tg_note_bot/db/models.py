"""
Implements db models.

.. class:: Users(Base)
.. class:: Rubrics(Base)
.. class:: Links(Base)
"""

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship
)


Base = declarative_base()


class User(Base):
    """ Implements telegram user model """

    __tablename__ = 'users'

    # basically, it supposed to be a telegram id
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    rubrics = relationship('Rubric', back_populates='user')
    links = relationship('Link', back_populates='user')

    def __repr__(self):
        return f'User(id={self.id!r}, created_at={self.created_at!r})'


class Rubric(Base):
    """ Implements link rubrics model """

    __tablename__ = 'rubrics'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='rubrics')
    links = relationship('Link', back_populates='rubric')

    def __repr__(self):
        return (
            f'Rubric(id={self.id!r}, name={self.name!r}, description={self.description!r}, '
            f'created_at={self.created_at!r}, user_id={self.user_id!r})'
        )


class Link(Base):
    """ Implements link model """

    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rubric_id = Column(Integer, ForeignKey('rubrics.id', ondelete='SET NULL'))

    user = relationship('User', back_populates='links')
    rubric = relationship('Rubric', back_populates='links')

    def __repr__(self):
        return (
            f'Link(id={self.id!r}, link={self.url!r}, description={self.description!r}, '
            f'created_at={self.created_at!r}, user_id={self.user_id!r}, rubric_id={self.rubric_id})'
        )

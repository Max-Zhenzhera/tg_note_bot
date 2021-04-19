"""
Implements db models.

.. class:: Users(Base)
.. class:: Rubrics(Base)
.. class:: Links(Base)

.. class:: Bug(Base)
"""

from aiogram.utils import markdown as md

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Sequence,
    func,
    BigInteger,
    Integer,
    String,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship
)
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.orm.exc import DetachedInstanceError


Base = declarative_base()


class User(Base):
    """ Implements telegram user model """

    __tablename__ = 'users'

    # basically, it supposed to be a telegram id
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    rubrics = relationship('Rubric', back_populates='user', order_by='Rubric.name')
    links = relationship('Link', back_populates='user', order_by='Link.url')

    def __repr__(self):
        return f'User(id={self.id!r}, created_at={self.created_at!r})'


class Rubric(Base):
    """ Implements link rubrics model """

    __tablename__ = 'rubrics'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='rubrics')
    links = relationship('Link', back_populates='rubric', order_by='Link.url')

    def __repr__(self):
        return (
            f'Rubric(id={self.id!r}, name={self.name!r}, description={self.description!r}, '
            f'created_at={self.created_at!r}, user_id={self.user_id!r})'
        )

    @property
    def bold_name(self) -> str:
        """ Return bold name of the rubric """
        return md.hbold(self.name)

    @property
    def name_with_description(self) -> str:
        """ Return short repr with description in square brackets if exists """
        return md.text(self.name, f'[{self.description}]') if self.description else self.name

    @property
    def bold_name_with_description(self) -> str:
        """ Return short repr with description in square brackets if exists """
        return md.text(self.bold_name, f'[{self.description}]') if self.description else self.bold_name

    def repr_with_links(self, link_shift: str, *, rubric_shift: str = '', links: list['Link'] = None) -> str:
        """
        Return formatted list of the rubric links with rubric name as title.
        Requires links loading or passing as argument.

        :param link_shift: shift string before link
        :type link_shift: str

        :keyword rubric_shift: shift string before rubric and before link shift
        :type rubric_shift: str
        :keyword links: links of have not loaded with rubric
        :type links: list[Link]

        :return: formatted list of the rubric links
        :rtype: str

        :raises MissingGreenlet: raised if rubric was not loaded with links
        """

        rubric_links = links if links else self.links

        link_shift = '\t' * 8 + link_shift

        text = md.text(
            f'{rubric_shift} {self.bold_name_with_description}',
            *[
                f'{link_shift} {link.short_url_with_description}'
                for link in rubric_links
            ],
            sep='\n'
        )

        return text


class Link(Base):
    """ Implements link model """

    __tablename__ = 'links'

    id = Column(BigInteger, primary_key=True)
    url = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    rubric_id = Column(BigInteger, ForeignKey('rubrics.id', ondelete='SET NULL'))

    user = relationship('User', back_populates='links')
    rubric = relationship('Rubric', back_populates='links')

    def __repr__(self):
        return (
            f'Link(id={self.id!r}, url={self.url!r}, description={self.description!r}, '
            f'created_at={self.created_at!r}, user_id={self.user_id!r}, rubric_id={self.rubric_id})'
        )

    @property
    def short_url(self) -> str:
        """ Delete http(s)://www. from url """
        return self.url.removeprefix('http://').removeprefix('https://').removeprefix('www.')

    @property
    def short_url_with_description(self) -> str:
        """ Hide link in the description if exists else hide link displaying in url """
        if self.description:
            text = md.text(self.description, f'[{self.short_url}]', sep='\n')
        else:
            text = self.short_url

        return text

    @property
    def short_url_with_description_and_rubric(self) -> str:
        """
        Add before `bold_name` property rubric name in square brackets if exists.
        Requires rubric loading.

        :raises MissingGreenlet: raised if link was not loaded with rubric
        """

        if self.rubric:
            text = md.text(self.rubric.name, '|', self.short_url_with_description)
        else:
            text = md.text('🖤', '|', self.short_url_with_description)

        return text


class Bug(Base):
    """ Implements db table for bugs keeping """

    __tablename__ = 'bugs'

    id = Column(BigInteger, primary_key=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    is_shown = Column(Boolean, server_default='false')

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return (
            f'Bug(id={self.id!r}, message={self.message!r}, created_at={self.created_at!r}, '
            f'is_shown={self.is_shown!r}, user_id={self.user_id!r})'
        )

    @property
    def tg_repr(self) -> str:
        """ Return detailed bug tg representation """
        return md.text(
            f'id: {self.id}'
            f'message: {self.message}',
            f'created at: {self.created_at.isoformat(" ")}',
            f'is shown before: {self.is_shown}',
            sep='\n'
        )

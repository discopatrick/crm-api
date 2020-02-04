from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from crm.database import Base


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    emails = relationship('Email', cascade='all, delete-orphan')


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(254))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
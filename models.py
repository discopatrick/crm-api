from sqlalchemy import Column, Integer, String

from database import Base


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))

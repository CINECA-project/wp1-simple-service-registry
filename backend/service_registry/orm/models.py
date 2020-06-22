"""
SQLAlchemy models for the database
"""
import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy import UniqueConstraint
from service_registry.orm.guid import GUID
from service_registry.orm import Base


class URL(Base):
    """
    SQLAlchemy class/table representing URL of a service
    """
    __tablename__ = 'urls'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    url = Column(String(100))
    added = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("url"),
    )

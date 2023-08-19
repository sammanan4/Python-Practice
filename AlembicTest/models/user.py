import re
import asyncio
import datetime
from enum import Enum
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import (
    String
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import validates

from .base import Base

class GenderType(Enum):
    male = "Male"
    female = "Female"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(20))
    gender: Mapped[GenderType]
    date_of_birth: Mapped[datetime.date]


    @validates('email')
    def validate_email(self, key, value):
        if re.match(r'^[\w][\w\d]{3,}@(gmail|ymail)\.(in|com|org)$', value) is None:
            raise ValueError('Invalid email provided')
        return value
    

    @validates('date_of_birth')
    def validate_date_of_birth(self, key, value):
        if value > datetime.date.today():
            raise ValueError('Date of birth cannot be in the future')
        return value
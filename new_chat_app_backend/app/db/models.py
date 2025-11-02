from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from datetime import datetime
from .base import Base
import enum

class GroupModelEnum(str, enum.Enum):
    PRIVATE = "private"
    ROOM = "room"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bio = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    g_id = Column(Integer, ForeignKey('groups.id', ondelete= "CASCADE", name='fk_group_id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete= "CASCADE", name='fk_sender_id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=False)
    model = Column(Enum(GroupModelEnum), default=GroupModelEnum.PRIVATE)

class Group_Mem(Base):
    __tablename__ = "group_members"

    g_id = Column(Integer, ForeignKey('groups.id', ondelete= "CASCADE", name='fk_group_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete= "CASCADE", name='fk_user_id'), primary_key=True)


import uuid
from sqlalchemy import Column, UUID, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from bot.app_database.database import Base

class UserState(Base): 
    __tablename__ = "user_state"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    state_id = Column(String, ForeignKey("user_state.id"))
    user_state = relationship("UserState")

    username = Column(String)
    isMen = Column(Boolean,default=True)

class TwitterUserModel(Base):
    __tablename__ = "twitter_users"

    id = Column(String, primary_key=True, index=True)
    state_id = Column(String, ForeignKey("user_state.id"))
    user_state = relationship("UserState")

    username = Column(String)
    isMen = Column(Boolean,default=True)
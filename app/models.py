from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    UserID: Optional[int] = Field(default=None, primary_key=True)
    Username: str
    Email: str
    PasswordHash: str
    ProfilePicture: Optional[str] = None
    Bio: Optional[str] = None
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

class Tweet(SQLModel, table=True):
    TweetID: Optional[int] = Field(default=None, primary_key=True)
    UserID: int = Field(foreign_key="user.UserID")
    Content: str
    MediaURL: Optional[str] = None
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

class Retweet(SQLModel, table=True):
    RetweetID: Optional[int] = Field(default=None, primary_key=True)
    TweetID: int = Field(foreign_key="tweet.TweetID")
    UserID: int = Field(foreign_key="user.UserID")
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

class Like(SQLModel, table=True):
    LikeID: Optional[int] = Field(default=None, primary_key=True)
    TweetID: int = Field(foreign_key="tweet.TweetID")
    UserID: int = Field(foreign_key="user.UserID")
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

class Follow(SQLModel, table=True):
    FollowerID: int = Field(foreign_key="user.UserID", primary_key=True)
    FolloweeID: int = Field(foreign_key="user.UserID", primary_key=True)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

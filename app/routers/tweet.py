from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Tweet
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Tweet)
def create_tweet(tweet: Tweet, session: Session = Depends(get_session)):
    db_tweet = Tweet(
        Content=tweet.Content,
        UserID=tweet.UserID,
        MediaURL=tweet.MediaURL,
        CreatedAt=datetime.utcnow(),
    )
    session.add(db_tweet)
    session.commit()
    session.refresh(db_tweet)
    return db_tweet

@router.get("/{tweet_id}", response_model=Tweet)
def read_tweet(tweet_id: int, session: Session = Depends(get_session)):
    tweet = session.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet

@router.delete("/{tweet_id}")
def delete_tweet(tweet_id: int, session: Session = Depends(get_session)):
    tweet = session.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    session.delete(tweet)
    session.commit()
    return {"detail": "Tweet deleted"}

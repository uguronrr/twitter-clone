from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Retweet
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Retweet)
def create_retweet(retweet: Retweet, session: Session = Depends(get_session)):
    db_retweet = Retweet(
        TweetID=retweet.TweetID,
        UserID=retweet.UserID,
        CreatedAt=datetime.utcnow(),
   
    )
    session.add(db_retweet)
    session.commit()
    session.refresh(db_retweet)
    return db_retweet

@router.delete("/{retweet_id}")
def delete_retweet(retweet_id: int, session: Session = Depends(get_session)):
    retweet = session.get(Retweet, retweet_id)
    if not retweet:
        raise HTTPException(status_code=404, detail="Retweet not found")
    session.delete(retweet)
    session.commit()
    return {"detail": "Retweet deleted"}
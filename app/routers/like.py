from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Like
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Like)
def create_like(like: Like, session: Session = Depends(get_session)):
    db_like = Like(
        TweetID=like.TweetID,
        UserID=like.UserID,
        CreatedAt=datetime.utcnow(),
    )
    session.add(db_like)
    session.commit()
    session.refresh(db_like)
    return db_like

@router.delete("/{like_id}")
def delete_like(like_id: int, session: Session = Depends(get_session)):
    like = session.get(Like, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    session.delete(like)
    session.commit()
    return {"detail": "Like deleted"}

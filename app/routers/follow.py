from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Follow
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Follow)
def create_follow(follow: Follow, session: Session = Depends(get_session)):
    db_follow = Follow(
        FollowerID=follow.FollowerID,
        FolloweeID=follow.FolloweeID,
        CreatedAt=datetime.utcnow(),
    )
    session.add(db_follow)
    session.commit()
    session.refresh(db_follow)
    return db_follow

@router.delete("/{follower_id}/{followee_id}")
def delete_follow(follower_id: int, followee_id: int, session: Session = Depends(get_session)):
    follow = session.exec(
        select(Follow).where(Follow.FollowerID == follower_id, Follow.FolloweeID == followee_id)
    ).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    session.delete(follow)
    session.commit()
    return {"detail": "Unfollowed successfully"}

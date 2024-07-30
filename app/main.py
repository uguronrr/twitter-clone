from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import auth, user, tweet, retweet, like, follow

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(tweet.router, prefix="/tweets", tags=["tweets"])
app.include_router(retweet.router, prefix="/retweets", tags=["retweets"])
app.include_router(like.router, prefix="/likes", tags=["likes"])
app.include_router(follow.router, prefix="/follows", tags=["follows"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Twitter Clone API"}

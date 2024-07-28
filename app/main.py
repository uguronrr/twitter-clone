from fastapi import FastAPI

app = FastAPI()

@app.get("/tweets")
async def read_tweets():
    pass

@app.post("/tweets")
async def create_tweet():
    pass

@app.get("/tweets/{tweet_id}")
async def read_tweet(tweet_id: int):
    pass

@app.put("/tweets/{tweet_id}")
async def update_tweet(tweet_id: int):
    pass

@app.delete("/tweets/{tweet_id}")
async def delete_tweet(tweet_id: int):
    pass

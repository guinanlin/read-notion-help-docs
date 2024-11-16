from fastapi import APIRouter, HTTPException
from app.services.tweets_service import get_tweet_by_id, get_sol_token_by_id
from app.utils.tweets import content_to_Embedding, content_to_Embedding2

router = APIRouter()

@router.get("/hello", response_model=dict, tags=["tweets"])
async def hello_world():
    return {"message": "Hello, World!"}

@router.get("/tweets/{tweet_id}", response_model=dict, tags=["tweets"])
async def get_tweet(tweet_id: int):
    tweet = get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet

@router.post("/tweets/split/{tweet_id}", tags=["tweets"])
async def split_tweet_content(tweet_id: int):
    tweet = get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    text_content = tweet.get("text", "")
    split_texts = split_content_function(text_content)

    for content in split_texts:
        insert_sol_tweet_document(ref_id=tweet_id, content=content)

    return {"message": "Tweet content split and stored successfully."}

@router.post("/tweets/embedding/{tweet_id}", tags=["tweets"])
async def update_tweet_embedding(tweet_id: int):
    tweet = get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    content = tweet.get("text", "")
    success = await content_to_Embedding(tweet_id=tweet_id, content=content)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update embedding")
    
    return {"message": "Embedding updated successfully."}

@router.post("/tokens/embedding/{token_id}", tags=["tweets"])
async def update_token_embedding(token_id: int):
    token = get_sol_token_by_id(token_id)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    name = token.get("name", "")
    symbol = token.get("symbol", "")
    content = f"name: {name}, symbol: {symbol}"

    success = await content_to_Embedding2(token_id=token_id, content=content)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update token embedding")
    
    return {"message": "Token embedding updated successfully."}
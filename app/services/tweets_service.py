from app.services.supabase import supabase

def get_tweet_by_id(tweet_id: int):
    response = supabase.table("tweets").select("*").eq("id", tweet_id).execute()
    return response.data[0] if response.data else None

def insert_sol_tweet_document(ref_id: int, content: str):
    response = supabase.table("sol_tweets_documents").insert({
        "ref_id": ref_id,
        "content": content
    }).execute()
    return response

def get_sol_token_by_id(token_id: int):
    response = supabase.table("sol_tokens").select("*").eq("id", token_id).execute()
    return response.data[0] if response.data else None
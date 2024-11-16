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

def get_tweets(skip: int, limit: int):
    # 获取总记录数
    total_response = supabase.table("tweets").select("id").execute()
    total_items = len(total_response.data) if total_response.data else 0
    total_pages = (total_items + limit - 1) // limit  # 计算总页数

    # 获取当前页的推文
    response = supabase.table("tweets").select(
        "id, created_at, username, time, tweetid, text, judgmentCode, result"
    ).order("time", desc=True).range(skip, skip + limit - 1).execute()
    
    data = response.data if response.data else []

    return {
        "meta": {
            "current_page": (skip // limit) + 1,  # 计算当前页
            "per_page": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": (skip + limit) < total_items,
            "has_previous": skip > 0,
        },
        "data": data
    }
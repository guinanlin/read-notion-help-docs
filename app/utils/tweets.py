import google.generativeai as genai
from app.services.supabase import SupabaseService

async def content_to_Embedding(tweet_id: int, content: str):
    model = 'models/text-embedding-004'
    
    try:
        # 生成embedding
        embedding_response = genai.embed_content(
            model=model,
            content=content,
            task_type="retrieval_document"
        )
        
        if embedding_response and 'embedding' in embedding_response:
            # 提取嵌入向量
            embedding = embedding_response['embedding']
            
            # 更新到Supabase的tweets表
            SupabaseService.update_tweet_embedding(tweet_id=tweet_id, embedding=embedding)
            return True
            
        return False
    except Exception as e:
        print(f"生成或存储嵌入向量时发生错误: {str(e)}")
        return False

async def content_to_Embedding2(token_id: int, content: str):
    model = 'models/text-embedding-004'
    
    try:
        # 生成embedding
        embedding_response = genai.embed_content(
            model=model,
            content=content,
            task_type="retrieval_document"
        )
        
        if embedding_response and 'embedding' in embedding_response:
            # 提取嵌入向量
            embedding = embedding_response['embedding']
            
            # 更新到Supabase的tokens表
            SupabaseService.update_token_embedding(token_id=token_id, embedding=embedding)
            return True
            
        return False
    except Exception as e:
        print(f"生成或存储嵌入向量时发生错误: {str(e)}")
        return False

async def from_content_to_Embedding(content: str):
    model = 'models/text-embedding-004'
    
    try:
        # 生成embedding
        embedding_response = genai.embed_content(
            model=model,
            content=content,
            task_type="retrieval_document"
        )
        
        if embedding_response and 'embedding' in embedding_response:
            # 提取嵌入向量
            embedding = embedding_response['embedding']
            return {"embedding": embedding}  # 返回嵌入向量
            
        return {"embedding": None}  # 如果没有生成嵌入向量
    except Exception as e:
        print(f"生成嵌入向量时发生错误: {str(e)}")
        return {"embedding": None}  # 返回 None

async def from_content_to_Embedding2(name: str, symbol: str):
    model = 'models/text-embedding-004'
    content = f"name: {name}, symbol: {symbol}"  # 拼接内容
    
    try:
        # 生成embedding
        embedding_response = genai.embed_content(
            model=model,
            content=content,
            task_type="retrieval_document"
        )
        
        if embedding_response and 'embedding' in embedding_response:
            # 提取嵌入向量
            embedding = embedding_response['embedding']
            return {"embedding": embedding}  # 返回嵌入向量
            
        return {"embedding": None}  # 如果没有生成嵌入向量
    except Exception as e:
        print(f"生成嵌入向量时发生错误: {str(e)}")
        return {"embedding": None}  # 返回 None

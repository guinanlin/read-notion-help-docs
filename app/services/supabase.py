from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional
import uuid

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 Supabase URL 和密钥
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# 创建 Supabase 客户端
supabase = create_client(supabase_url, supabase_key)

class SupabaseService:
    @staticmethod
    async def get_table_data(table_name: str, fields: List[str] = None, limit: int = None) -> List[Dict[str, Any]]:
        """
        从指定的表中获取所有数据
        
        Args:
            table_name: 表名
            fields: 要读取的字段列表，默认为 None 以读取所有字段
            limit: 限制返回的记录数，默认为 None 以返回所有记录
            
        Returns:
            List[Dict]: 表中的所有数据
            
        Raises:
            Exception: 当获取数据失败时抛出异常
        """
        # 如果未指定字段，则使用 *
        selected_fields = ",".join(fields) if fields else "*"
        query = supabase.table(table_name).select(selected_fields)
        
        # 如果指定了 limit，则添加到查询中
        if limit is not None:
            query = query.limit(limit)
        
        response = query.execute()
        if response.data is None:
            return []
        return response.data 

    @staticmethod
    async def insert_data(table_name: str, data: Dict[str, Any]) -> None:
        """
        插入数据到指定表
        
        Args:
            table_name: 表名
            data: 要插入的数据
        """
        supabase.table(table_name).insert(data).execute()

    @staticmethod
    async def insert_document_embedding(
        content: str,
        embedding: List[float],
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        将文档内容、embedding和元数据插入到notion_documents表
        
        Args:
            content: 文档内容
            embedding: 文档的embedding向量
            metadata: 文档的元数据，如标题、URL等
        """
        document_data = {
            "id": str(uuid.uuid4()),
            "content_id": str(uuid.uuid4()),
            "content": content,
            "metadata": metadata or {},
            "embedding": embedding
        }
        
        try:
            supabase.table("notion_documents").insert(document_data).execute()
        except Exception as e:
            print(f"插入文档embedding时发生错误: {str(e)}")
            raise e
            
    @staticmethod
    async def insert_docs_directory(directory: List[Dict[str, Any]], parent_id: uuid.UUID = None, level: int = 0) -> None:
        """
        插入目录结构到 n_docs_directory 表
        
        Args:
            directory: 目录结构的列表
            parent_id: 父级目录的 ID
            level: 当前目录的层级
        """
        for item in directory:
            # 生成唯一的 ID
            item_id = str(uuid.uuid4())
            
            # 准备数据
            data = {
                "id": item_id,
                "title": item["title"],
                "url": item.get("url"),  # 使用 get() 以防没有 url
                "parent_id": str(parent_id) if parent_id else None,
                "level": level
            }
            
            # 插入数据到 Supabase
            await SupabaseService.insert_data("n_docs_directory", data)
            
            # 如果有子项，递归插入
            if "items" in item and item["items"]:
                await SupabaseService.insert_docs_directory(item["items"], item_id, level + 1)
                
    @staticmethod
    async def insert_docs_content(content: List[Dict[str, Any]]) -> None:
        """
        插入文档内容到 n_docs_content 表
        """
        supabase.table("n_docs_content").insert(content).execute()
    
    @staticmethod
    async def insert_docs_split_content(content: List[Dict[str, Any]]) -> None:
        """
        插入文档内容到 n_docs_split_content 表
        """
        print(f"content: {content}")
        try:
            # 插入数据
            response = supabase.table("notion_documents").insert(content).execute()
            if response.status_code != 201:  # 检查是否插入成功
                raise Exception(f"插入失败: {response.json()}")
        except Exception as e:
            print(f"插入数据时发生错误: {str(e)}")
            raise e  # 重新抛出异常以便上层调用可以处理

    @staticmethod
    def update_tweet_embedding(tweet_id: int, embedding: list):
        response = supabase.table("tweets").update({
            "embedding": embedding
        }).eq("id", tweet_id).execute()
        return response
    
    @staticmethod
    def update_token_embedding(token_id: int, embedding: list):
        response = supabase.table("sol_tokens").update({
            "embedding": embedding
        }).eq("id", token_id).execute()
        return response

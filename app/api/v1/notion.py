from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import get_current_active_user
from app.models.user import User
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from app.services.supabase import SupabaseService
from app.services.notion_service import NotionService
from app.models.notion import NotionHelpSection
import uuid
from app.utils.notion import split_content_function
router = APIRouter()

# 定义响应模型
class NotionDirectory(BaseModel):
    id: int
    created_at: datetime
    directory: str | None
    url: str | None

class NotionHelpSection(BaseModel):
    title: str
    subtitle: str | None = None
    items: List[Dict] = []

class NotionHelpArticle(BaseModel):
    title: str
    breadcrumbs: List[Dict[str, str]]
    content: str
    video_url: str | None = None
    next_article: Dict[str, str] | None = None

@router.get("/notion/get-directory", response_model=List[NotionDirectory], tags=["Notion"])
async def get_notion_data(current_user: User = Depends(get_current_active_user)):
    try:
        # 使用 SupabaseService 获取数
        data = await SupabaseService.get_table_data('notion_directory')
        
        if not data:
            raise HTTPException(status_code=404, detail="没有找到数据")
            
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据失败: {str(e)}")

@router.post("/notion/get-notion-help-directory", response_model=List[NotionHelpSection], tags=["Notion"])
async def get_notion_help_directory(
    current_user: User = Depends(get_current_active_user),
    operator: str = "Query"
):
    """
    获取 Notion 帮助目录。

    该接口从 Notion 服务获取帮助目录。如果指定的操作为 "Insert"，则将目录插入到数据库中。

    请求方法:
        POST

    请求路径:
        /notion/get-notion-help-directory

    请求参数:
        - current_user (User): 当前活动用户，使用依赖注入获取。
        - operator (str): 操作类型，默认为 "Query"。如果为 "Insert"，则将目录插入到数据库。

    返回:
        List[NotionHelpSection]: 包含 Notion 帮助目录的列表。如果没有找到帮助目录，则返回空列表。

    异常:
        - HTTPException: 如果在处理帮助目录时发生错误，将返回 500 状态码和错误信息。

    注意:
        - 确保在调用此接口之前，Notion 服务可用并且能够获取帮助目录。
    """
    try:
        # 获取 Notion 帮助目录
        sections = NotionService.fetch_notion_help_directory()
        
        # 判断 sections 是否为 None 或者为空
        if not sections:  # 如果 sections 为 None 或者空列表
            return []  # 直接返回空列表
        
        # 只有当 operator 为 "Insert" 时，才调用插入方法
        if operator == "Insert":
            # 转换 sections 为适合插入的格式
            insert_data = []
            for section in sections:
                section_data = {
                    "id": str(uuid.uuid4()),
                    "title": section.title,
                    "subtitle": section.subtitle,
                    "items": section.items
                }
                insert_data.append(section_data)
            await SupabaseService.insert_docs_directory(insert_data)  # 调用插入方法
        
        return sections
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理Notion帮助目录失败: {str(e)}")

@router.post("/notion/get-notion-help-article", response_model=NotionHelpArticle, tags=["Notion"])
async def get_notion_help_article(
    url: str = "https://www.notion.com/help/start-here",
    current_user: User = Depends(get_current_active_user)
):
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, 
                              detail=f"获取Notion帮助文章失败: {response.status_code}")
        
        # 调用 NotionService 解析文章内容
        article_data = await NotionService.parse_notion_help_article(response.text)
        
        return article_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理Notion帮助文章失败: {str(e)}")

@router.post("/notion/insert-docs-content", tags=["Notion"])
async def insert_docs_content(current_user: User = Depends(get_current_active_user)):
    """
    从 n_docs_directory 表中读取目录数据，并插入文档内容到数据库。

    该接口会从 n_docs_directory 表中获取 URL 列表，访问每个 URL，解析 Notion 帮助文章的内容，
    然后将解析后的数据插入到数据库 n_docs_content 中。

    请求方法:
        POST

    请求路径:
        /notion/insert-docs-content

    请求参数:
        - current_user (User): 当前活动用户，使用依赖注入获取。

    请求示例:
        curl -X POST "http://<your-api-url>/notion/insert-docs-content" \
        -H "Authorization: Bearer <your-token>"

    返回:
        dict: 包含操作结果的字典，例如 {"result": "所有文档内容插入成功"} 或 {"result": "没有目录数据"}。

    异常:
        - HTTPException: 如果在插入文档内容时发生错误，将返回 500 状态码和错误信息。

    注意:
        - 确保在调用此接口之前，n_docs_directory 表中有可用的 URL 数据。
        - 此接口需要有效的用户身份验证。
    """
    try:
        # 读取 n_docs_directory 表
        directory_data = await SupabaseService.get_table_data("n_docs_directory", fields=["url"], limit=5)

        # 确保目录数据不为空
        if directory_data:
            for directory in directory_data:  # 循环所有目录项
                url = directory.get("url")  # 使用 get 方法获取 url
                
                if url:  # 检查 url 是否为 None
                    try:
                        response = requests.get("https://www.notion.com" + url)
                        article_data = await NotionService.parse_notion_help_article(response.text)

                        # 准备插入的数据
                        data_to_insert = {
                            "title": article_data.title,
                            "content": article_data.content,
                            "description": article_data.next_article.get("description") if article_data.next_article else None,
                            "metadata": {
                                "breadcrumbs": article_data.breadcrumbs,
                                "video_url": article_data.video_url,
                                "next_article": article_data.next_article
                            }
                        }

                        # 插入文档内容
                        await SupabaseService.insert_docs_content(data_to_insert)  # 使用准备好的数据
                    except Exception as inner_e:
                        print(f"处理 URL {url} 时出错: {str(inner_e)}")  # 打印错误信息
            
            return {"result": "所有文档内容插入成功"}
        
        return {"result": "没有目录数据"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"插入文档内容失败: {str(e)}")

@router.post("/notion/insert-docs-split-content", tags=["Notion"])
async def insert_docs_split_content(current_user: User = Depends(get_current_active_user)):
    """
    插入文档分割内容到 notion_documents 表。

    该接口从 n_docs_content 表中读取内容，使用 `split_content_function` 函数对内容进行分割，
    然后将分割后的内容插入到 notion_documents 表中。

    请求方法:
        POST

    请求路径:
        /notion/insert-docs-split-content

    请求参数:
        - current_user (User): 当前活动用户，使用依赖注入获取。

    请求示例:
        curl -X POST "http://<your-api-url>/notion/insert-docs-split-content" \
        -H "Authorization: Bearer <your-token>"

    返回:
        dict: 包含操作结果的字典，例如 {"result": "success"}。

    异常:
        - 可能会抛出异常，如果在插入数据时发生错误，将打印错误信息并返回 500 状态码。

    注意:
        - 确保在调用此接口之前，n_docs_content 表中有可用的数据。
        - 此接口需要有效的用户身份验证。
    """
    # 读取 n_docs_content 表
    content_data = await SupabaseService.get_table_data("n_docs_content", fields=["id", "content", "metadata"])
    
    # 循环 content_data 数据
    for content in content_data:
        # 将 content 转换为字符串
        content_str = str(content["content"])
        
        # 调用 split_content 函数，假设它返回一个包含 content_id、content 和 metadata 的字典列表
        split_result = split_content_function(content_str)
        
        split_result_array = []
        # 确保 split_result 中的每个项都包含所需的字段
        for item in split_result:
            doc = {}  # 在这里定义 doc
            doc["content_id"] = content["id"]  # 使用 content_id
            doc["metadata"] = content["metadata"]  # 使用 metadata
            doc["content"] = item
            
            split_result_array.append(doc)
        try:
            await SupabaseService.insert_docs_split_content(split_result_array)  # 将 doc 作为列表传递
        except Exception as e:
            print(f"插入数据时发生错误: {str(e)}")
    
    return {"result": "success"}

@router.post("/notion/get-notion-help-article-split-content", response_model=NotionHelpArticle, tags=["Notion"])
async def get_notion_help_article_split_content(url: str, current_user: User = Depends(get_current_active_user)):
    return {"result": "success"}
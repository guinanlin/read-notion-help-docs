import google.generativeai as genai
import os
from app.services.supabase import SupabaseService

# 在文件开头添加配置
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def split_content_function(content):
    # 以段落为单位分割内容
    paragraphs = content.split('\n\n')
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # 去掉首尾空白
        paragraph = paragraph.strip()
        
        # 如果当前块加上新段落会超过字符限制
        if len(current_chunk) + len(paragraph) + 2 > 750:  # +2 是因为需要添加换行
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n"  # 开始新的块
        
        else:
            current_chunk += paragraph + "\n"  # 继续添加到当前块

    # 添加最后一个块
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

async def content_to_Embedding(title: str, content: str, metadata: dict = None):
    """
    使用Google Gemini的text-embedding-004模型生成文本嵌入向量并存储到Supabase
    
    Args:
        title (str): 文档标题
        content (str): 文档内容
        metadata (dict): 额外的元数据信息
        
    Returns:
        bool: 是否成功处理
    """
    model = 'models/text-embedding-004'
    
    try:
        # 生成embedding
        embedding_response = genai.embed_content(
            model=model,
            content=content,
            task_type="retrieval_document",
            title=title
        )
        
        if embedding_response and 'embedding' in embedding_response:
            # 提取嵌入向量
            embedding = embedding_response['embedding']
            
            # 准备元数据
            full_metadata = {
                "title": title,
                **(metadata or {})  # 合并额外的元数据
            }
            
            # 存储到Supabase
            await SupabaseService.insert_document_embedding(
                content=content,
                embedding=embedding,  # 只传递嵌入向量数组
                metadata=full_metadata
            )
            return True
            
        return False
    except Exception as e:
        print(f"生成或存储嵌入向量时发生错误: {str(e)}")
        return False

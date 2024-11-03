# 项目名称

项目描述：这是一个用于处理 Notion 帮助文档的 API 服务，支持从 Notion 获取帮助目录、插入文档内容、并且对文档进行分段处理， 最终以768维度存储到数据库。同时项目在FastAPI端实现了 Oauth2.

当前为开发调试版本，还有如下一些关键问题待解决。 

1. ​	对主体的文档的抽取还待细化， 以支持更灵活的抽取。
2.    向量文本的插入 app\utils\notion.py 的 content_to_Embedding 方法， 暂未整合进去。 
3.    对文档的解析， 分段， 向量存储 为提升能力， 还需做多线程处理。 

## 技术栈

| 库名                          | 主要用途                                               |
|------------------------------|------------------------------------------------------|
| fastapi                       | 构建快速的API，支持异步编程和自动生成文档。            |
| uvicorn[standard]            | ASGI服务器，用于运行FastAPI应用。                     |
| python-multipart              | 处理表单数据，支持文件上传。                           |
| python-jose[cryptography]    | 处理JSON Web Tokens (JWT)的创建和验证。              |
| passlib[bcrypt]              | 提供密码哈希和验证功能，支持多种算法。                  |
| python-jose                   | 处理JWT的创建和验证，轻量级库。                        |
| pytest                        | 测试框架，用于编写和运行测试。                         |
| httpx                        | 发送HTTP请求，支持异步和同步调用。                     |
| requests                     | 简化HTTP请求的库，支持多种HTTP方法。                  |
| bcrypt                       | 提供密码哈希功能，基于bcrypt算法。                     |
| supabase==2.9.1              | 与Supabase进行交互的客户端库，简化数据库操作。         |
| realtime==2.0.6              | Supabase实时功能的客户端库，支持实时数据更新。         |
| gotrue==2.9.3                | Supabase的身份验证服务客户端库，管理用户认证。         |
| storage3==0.8.2              | Supabase存储服务的客户端库，支持文件管理。             |
| postgrest==0.17.2            | 提供与PostgREST的接口，简化数据库操作。                 |
| httpx==0.27.2                | HTTP客户端库，支持异步和同步请求（重复）。             |
| supafunc==0.6.2              | Supabase功能的支持库，简化特定功能的使用。              |
| aiohttp                      | 异步HTTP客户端，用于发送HTTP请求和接收响应。            |
| python-dotenv                | 加载环境变量的库，便于管理配置文件。                   |
| beautifulsoup4               | 用于解析和提取HTML/XML数据的库。                       |
| lxml                         | 解析和处理XML和HTML文档的高性能库。                    |
| google-generativeai          | 与Google生成式AI进行交互的库，用于向量文本的存储              |


## 目录

- [功能](#功能)
- [安装](#安装)
- [使用](#使用)
- [API 接口](#api-接口)
- [贡献](#贡献)
- [许可证](#许可证)

## 功能

- 从 Notion 获取帮助目录
- 插入文档内容到数据库
- 对每篇文档的主体内容进行分段， 最终以768维度的向量文本存储到数据库

结果：

![](https://pic.imgdb.cn/item/6726d46dd29ded1a8c235b62.png)

![image-20241103172341764](C:\Users\guinan.lin\AppData\Roaming\Typora\typora-user-images\image-20241103172341764.png)

![](https://pic.imgdb.cn/item/6726d4bed29ded1a8c238ee0.png)



![](https://pic.imgdb.cn/item/6726d4d7d29ded1a8c239f21.png)

![image-20241103172523259](C:\Users\guinan.lin\AppData\Roaming\Typora\typora-user-images\image-20241103172523259.png)

## 安装

1. 克隆项目到本地：

   ```bash
   git clone <项目的Git地址>
   ```

2. 进入项目目录：

   ```bash
   cd <项目目录>
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

4. 配置env：

   ```
   SUPABASE_URL=https://ghexx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXAV
   GOOGLE_API_KEY=AIzaSyA4eLav8
   ```

5. 启动服务

  ```
  $ uvicorn app.main:app --reload --host 0.0.0.0 --port 8020
  ```

6.  Oath2用户登录

   默认的授权账号：
   - 用户名：guinan
   - 密码：123456

   ```
   python app/utils/security.py
   ```

## 使用

1. 启动服务：

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8020
   ```

2. 访问 API 文档：

   打开浏览器并访问 `http://localhost:8020/docs`  查看 API 文档。

## API 接口

- 具体的接口查看：

  http://192.168.8.135:8020/redoc

- ## Get Notion Help Directory
  
  获取 Notion 帮助目录。
  
  该接口从 Notion 服务获取帮助目录。如果指定的操作为 "Insert"，则将目录插入到数据库中。
  
  请求方法: POST
  
  请求路径: /notion/get-notion-help-directory
  
  请求参数: - current_user (User): 当前活动用户，使用依赖注入获取。 - operator (str): 操作类型，默认为 "Query"。如果为 "Insert"，则将目录插入到数据库。
  
  返回: List[NotionHelpSection]: 包含 Notion 帮助目录的列表。如果没有找到帮助目录，则返回空列表。
  
  异常: - HTTPException: 如果在处理帮助目录时发生错误，将返回 500 状态码和错误信息。
  
  注意: - 确保在调用此接口之前，Notion 服务可用并且能够获取帮助目录。
  
- ## Insert Docs Content

  从 n_docs_directory 表中读取目录数据，并插入文档内容到数据库。

  该接口会从 n_docs_directory 表中获取 URL 列表，访问每个 URL，解析 Notion 帮助文章的内容， 然后将解析后的数据插入到数据库 n_docs_content 中。

  请求方法: POST

  请求路径: /notion/insert-docs-content

  请求参数: - current_user (User): 当前活动用户，使用依赖注入获取。

  请求示例: curl -X POST "http:///notion/insert-docs-content" -H "Authorization: Bearer "

  返回: dict: 包含操作结果的字典，例如 {"result": "所有文档内容插入成功"} 或 {"result": "没有目录数据"}。

  异常: - HTTPException: 如果在插入文档内容时发生错误，将返回 500 状态码和错误信息。

  注意: - 确保在调用此接口之前，n_docs_directory 表中有可用的 URL 数据。 - 此接口需要有效的用户身份验证。

- ## Insert Docs Split Content

  插入文档分割内容到 notion_documents 表。

  该接口从 n_docs_content 表中读取内容，使用 `split_content_function` 函数对内容进行分割， 然后将分割后的内容插入到 notion_documents 表中。

  请求方法: POST

  请求路径: /notion/insert-docs-split-content

  请求参数: - current_user (User): 当前活动用户，使用依赖注入获取。

  请求示例: curl -X POST "http:///notion/insert-docs-split-content" -H "Authorization: Bearer "

  返回: dict: 包含操作结果的字典，例如 {"result": "success"}。

  异常: - 可能会抛出异常，如果在插入数据时发生错误，将打印错误信息并返回 500 状态码。

  注意: - 确保在调用此接口之前，n_docs_content 表中有可用的数据。 - 此接口需要有效的用户身份验证。

## 贡献

欢迎任何形式的贡献！请提交问题、建议或拉取请求。

## 许可证

本项目采用 MIT 许可证，详细信息请查看 [LICENSE](LICENSE) 文件。
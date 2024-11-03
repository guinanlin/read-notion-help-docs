import pytest
from app.utils.notion import split_content, content_to_Embedding

# def test_split_content():
#     content = "Share any Notion page you create with select people, your whole team, or the entire web. It's up to you. Here's a quick overview of how to share 🗣\n\nYou can invite people inside or outside your workspace to share a Notion page with you.\n\nStart with your page in Private in your sidebar.\n\nOn the page, go to Share at the top right.\n\nEnter the person's name or email address in the space provided, choose a level of access, and click Invite.\n\nIf the person is outside your workspace, they'll join the page as a guest.\n\nIf the person is already a member of your workspace, you'll see their profile photo pop up in the invite menu, and the page will show up under Shared in your sidebar, as seen above.\n\nIf you have multiple people working with you in Notion, you can quickly share any page with all of them. There are several ways to do this:\n\nShare with everyone in your workspace. Click Share at the top right of the page, and grant access to Everyone at [workspace name]. You can also assign everyone in your workspace a particular access level from the dropdown. For example, everyone Can view instead of being able to edit.\n\nCreate a page in any default teamspace in your sidebar. Everyone in your workspace is a member of default teamspaces and will automatically have access to pages in them. Learn more about teamspaces →\n\nDrag a private page to a default teamspace in your sidebar. This automatically shares it with everyone.\n\nShare a page's URL. Every page in Notion has its own unique URL you can use to share it on Slack or elsewhere. Go to Share at the top right and click Copy link. Only people who have access to the page can see it.\n\nYou can easily turn your Notion page into a beautiful website with Notion Sites. Learn more about how to share your page with the web here →\n\n• If the person is outside your workspace, they'll join the page as a guest.\n• If the person is already a member of your workspace, you'll see their profile photo pop up in the invite menu, and the page will show up under Shared in your sidebar, as seen above.\n\n• Share with everyone in your workspace. Click Share at the top right of the page, and grant access to Everyone at [workspace name]. You can also assign everyone in your workspace a particular access level from the dropdown. For example, everyone Can view instead of being able to edit.\n• Create a page in any default teamspace in your sidebar. Everyone in your workspace is a member of default teamspaces and will automatically have access to pages in them. Learn more about teamspaces →\n• Drag a private page to a default teamspace in your sidebar. This automatically shares it with everyone.\n\n• Share a page's URL. Every page in Notion has its own unique URL you can use to share it on Slack or elsewhere. Go to Share at the top right and click Copy link. Only people who have access to the page can see it."

#     # 使用双换行符进行分割
#     result = split_content_function(content)

#     # 打印每个元素并插入分隔线
#     for item in result:
#         print(item)  # 打印每个元素
#         print("=====================")  # 插入分隔线

# pytest -s tests/test_notion.py::test_content_to_Embedding
@pytest.mark.asyncio
async def test_content_to_Embedding():
    title = 'test'
    content = 'This is a test content.'
    
    # 使用 await 调用 content_to_Embedding 函数
    result = await content_to_Embedding(title, content)

    # 打印结果
    print(result)

    # 进行断言，检查返回值是否为 True
    assert result is True  # 确保返回值是 True
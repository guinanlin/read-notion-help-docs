import requests
from bs4 import BeautifulSoup
from app.models.notion import NotionHelpSection, NotionHelpArticle  # 确保导入 NotionHelpSection 和 NotionHelpArticle 模型
from fastapi import HTTPException

class NotionService:
    @staticmethod
    def fetch_notion_help_directory() -> list:
        url = "https://www.notion.com/help"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, 
                                detail=f"获取Notion帮助页面失败: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'lxml')
        sections = []
        
        # 查找所有导航部分
        nav_sections = soup.find_all("section", class_="HelpCenterSidebarContent_navSection__fb5g3")
        
        for nav_section in nav_sections:
            # 获取部分标题信息
            title_section = nav_section.find("section", class_="HelpCenterSidebarContent_navSectionTitle__HHoQS")
            if not title_section:
                continue
                
            title_link = title_section.find("a", class_="HelpCenterSidebarContent_navTitleLink__PEEjz")
            if not title_link:
                continue
                
            # 提取标题和副标题
            title = title_link.find("span", class_="text_textWeightBold__NuyUS").get_text()
            subtitle_elem = title_link.find("span", class_="HelpCenterSidebarContent_navSubtitle__OR3nf")
            subtitle = subtitle_elem.get_text() if subtitle_elem else None
            
            section = NotionHelpSection(
                title=title,
                subtitle=subtitle,
                items=[]
            )
            
            # 获取该部分下的所有项目
            dl_lists = nav_section.find_all("dl", class_="toggleList_toggleList__X4yHc")
            for dl in dl_lists:
                # 获取主类别
                dt = dl.find("dt")
                if not dt:
                    continue
                    
                category_link = dt.find("a", class_="toggleList_link__safdF")
                if not category_link:
                    continue
                    
                category = {
                    "title": category_link.get_text(),
                    "url": category_link.get("href"),
                    "items": []
                }
                
                # 获取子项目
                for dd in dl.find_all("dd", class_="toggleList_toggleListDescription___3yk5"):
                    item_link = dd.find("a", class_="toggleList_link__safdF")
                    if item_link:
                        category["items"].append({
                            "title": item_link.get_text(),
                            "url": item_link.get("href")
                        })
                
                section.items.append(category)
            
            sections.append(section)
        
        return sections
    
    @staticmethod
    async def parse_notion_help_article(html_content: str):
        soup = BeautifulSoup(html_content, 'lxml')
        
        breadcrumbs = []
        for crumb in soup.find_all("li", class_="breadcrumbs_breadcrumbsCrumb__ngT_q"):
            link = crumb.find("a")
            if link:
                breadcrumbs.append({
                    "title": link.get_text(),
                    "url": link.get("href")
                })
        
        title_element = soup.find("h1", class_="title_title__DWL5N")
        title = title_element.get_text().strip() if title_element else "未知标题"
        
        video_url = None
        video_iframe = soup.find("iframe", class_="videoPlayer_videoIframe__ZNVrQ")
        if video_iframe:
            video_url = video_iframe.get("src")
        
        content_sections = []
        prologue = soup.find("h2", class_="helpArticle_helpArticlePrologueCopy__0cmaN")
        if prologue:
            content_sections.append(prologue.get_text().strip())
        
        article_content = soup.find("article", class_="contentfulRichText_richText__rW7Oq")
        if article_content:
            for paragraph in article_content.find_all("p", class_="contentfulRichText_paragraph___hjRE"):
                text = paragraph.get_text().strip()
                if text:
                    content_sections.append(text)
            for ul in article_content.find_all("ul", class_="contentfulRichText_list__89IEM"):
                list_items = []
                for li in ul.find_all("li"):
                    list_items.append(f"• {li.get_text().strip()}")
                if list_items:
                    content_sections.append("\n".join(list_items))
        
        next_article = None
        next_preview = soup.find("article", class_="helpCenterContentPreview_articlePreview__Epc1O")
        if next_preview:
            link = next_preview.find("a")
            title_elem = next_preview.find("h3", class_="title_title__DWL5N")
            description = next_preview.find("p", class_="text_text__cG3pf text_textWeightRegular__lAQvj text_textColorMedium__XD_3v text_textSizeBody__4q5Cs")
            if link and title_elem:
                next_article = {
                    "title": title_elem.get_text().strip(),
                    "url": link.get("href"),
                    "description": description.get_text().strip() if description else None
                }
        
        if not content_sections:
            content_sections = ["暂无内容"]
        
        return NotionHelpArticle(
            title=title,
            breadcrumbs=breadcrumbs,
            content="\n\n".join(content_sections),
            video_url=video_url,
            next_article=next_article
        )
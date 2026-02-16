#!/usr/bin/env python3
"""
Blog Post Fetcher for GitHub Profile README
Fetches latest blog posts from RSS feed and updates README.md
"""

import feedparser
import re
from datetime import datetime

RSS_URL = "https://jackie.openenet.cn/atom.xml"
README_PATH = "README.md"
MAX_POSTS = 5

def fetch_blog_posts():
    """Fetch latest blog posts from RSS feed"""
    try:
        feed = feedparser.parse(RSS_URL)
        posts = []
        
        for entry in feed.entries[:MAX_POSTS]:
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            published = entry.get('published', '')
            
            if published:
                try:
                    date_obj = datetime.strptime(published[:10], '%Y-%m-%d')
                    date_str = date_obj.strftime('%Y-%m-%d')
                except:
                    date_str = published[:10]
            else:
                date_str = ''
            
            posts.append({
                'title': title.strip(),
                'link': link.strip(),
                'date': date_str
            })
        
        return posts
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return None

def update_readme(posts):
    """Update README.md with latest blog posts"""
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not posts:
            new_section = """<!-- BLOG-POST-LIST:START -->
- ❌ 无法获取博客文章 / Unable to fetch blog posts
<!-- BLOG-POST-LIST:END -->"""
        else:
            post_lines = []
            for post in posts:
                date_prefix = f"📅 {post['date']} " if post['date'] else ""
                post_lines.append(
                    f"- {date_prefix}[{post['title']}]({post['link']})"
                )
            
            new_section = """<!-- BLOG-POST-LIST:START -->
""" + "\n".join(post_lines) + """
<!-- BLOG-POST-LIST:END -->"""
        
        pattern = r'<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->'
        new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Successfully updated {len(posts) if posts else 0} blog posts")
        return True
        
    except Exception as e:
        print(f"Error updating README: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Fetching latest blog posts...")
    posts = fetch_blog_posts()
    if posts:
        print(f"📝 Found {len(posts)} posts")
        update_readme(posts)
    else:
        print("❌ Failed to fetch blog posts")
        update_readme(None)

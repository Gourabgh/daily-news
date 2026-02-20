import feedparser
import os
from datetime import datetime
import re

# BBC News RSS Feed
rss_url = "http://feeds.bbci.co.uk/news/rss.xml"
feed = feedparser.parse(rss_url)

# The folder where the Dante theme keeps its blog posts
output_dir = "src/content/blog"
os.makedirs(output_dir, exist_ok=True)

# Grab the top 5 news stories
for entry in feed.entries[:5]:
    # Make a safe file name out of the title
    safe_title = re.sub(r'[^a-z0-9]', '-', entry.title.lower())
    safe_title = re.sub(r'-+', '-', safe_title).strip('-')
    filename = f"{safe_title}.md"
    filepath = os.path.join(output_dir, filename)

    # Format the date exactly how Astro wants it
    pub_date = datetime.now().strftime("%Y-%m-%d")
    clean_title = entry.title.replace('"', "'")
    clean_summary = entry.summary.replace('"', "'")

    # Create the Markdown format with 'publishDate' instead of 'pubDate'
    markdown_content = f"""---
title: "{clean_title}"
description: "{clean_summary}"
publishDate: {pub_date}
---

{clean_summary}

[Read the full story on BBC]({entry.link})
"""
    # Save the new article file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
print("News automatically generated!")

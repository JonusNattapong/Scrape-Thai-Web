import requests
import json
import re
from bs4 import BeautifulSoup

def clean_text(text):
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_comment_text(item):
    if not isinstance(item, dict):
        return None
    msg = item.get('message', '')
    # Remove HTML tags like <br />
    msg = re.sub(r'<[^>]+>', ' ', msg)
    return clean_text(msg)

def scrape_pantip_topic(topic_id):
    url = f"https://pantip.com/topic/{topic_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Fetching topic {topic_id}...")
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8' # Force UTF-8
    if response.status_code != 200:
        print(f"Failed to fetch topic: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title and summary from meta tags (cleaner than HTML)
    title = soup.find('meta', property='og:title')
    title = title['content'] if title else ""
    
    summary = soup.find('meta', property='og:description')
    summary = summary['content'] if summary else ""
    
    # Clean title and summary
    title = clean_text(title)
    summary = clean_text(summary)
    
    # Fetch comments
    comments_url = f"https://pantip.com/forum/topic/render_comments?tid={topic_id}"
    api_headers = headers.copy()
    api_headers['X-Requested-With'] = 'XMLHttpRequest'
    
    print(f"Fetching comments for topic {topic_id}...")
    comments_response = requests.get(comments_url, headers=api_headers)
    
    all_comments = []
    if comments_response.status_code == 200:
        try:
            # Handle UTF-8 BOM
            content = comments_response.content.decode('utf-8-sig')
            data = json.loads(content)
            comment_list = data.get('comments', [])
            for item in comment_list:
                # Main comment
                text = extract_comment_text(item)
                if text:
                    all_comments.append(text)
                
                # Replies
                replies = item.get('replies', [])
                for reply in replies:
                    reply_text = extract_comment_text(reply)
                    if reply_text:
                        all_comments.append(reply_text)
        except Exception as e:
            print(f"Error parsing comments JSON: {e}")
    else:
        print(f"Failed to fetch comments: {comments_response.status_code}")

    return {
        'topic_id': topic_id,
        'title': title,
        'summary': summary,
        'comments': all_comments
    }

if __name__ == "__main__":
    # Read topic URLs from list.txt
    try:
        with open('list.txt', 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: list.txt not found")
        exit(1)
    
    # Extract topic IDs from URLs
    topic_ids = []
    for url in urls:
        # Extract topic ID from URL like https://pantip.com/topic/43899619
        import re
        match = re.search(r'/topic/(\d+)', url)
        if match:
            topic_ids.append(match.group(1))
        else:
            print(f"Warning: Could not extract topic ID from {url}")
    
    if not topic_ids:
        print("No valid topic IDs found in list.txt")
        exit(1)
    
    output_file = "data/pantip_dataset.jsonl"
    
    # Scrape each topic and append to file
    total_topics = len(topic_ids)
    successful = 0
    
    for i, topic_id in enumerate(topic_ids, 1):
        print(f"\n[{i}/{total_topics}] Scraping topic {topic_id}...")
        result = scrape_pantip_topic(topic_id)
        
        if result:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
            successful += 1
            print(f"✓ Topic {topic_id}: {len(result['comments'])} comments")
        else:
            print(f"✗ Failed to scrape topic {topic_id}")
    
    print(f"\n{'='*50}")
    print(f"Scraping completed!")
    print(f"Total topics processed: {total_topics}")
    print(f"Successful: {successful}")
    print(f"Failed: {total_topics - successful}")
    print(f"Data saved to {output_file}")

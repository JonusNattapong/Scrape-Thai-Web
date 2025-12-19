#!/usr/bin/env python3
"""
YouTube Comment Scraper (Requests-based)
ดึงความคิดเห็นจากวิดีโอ YouTube โดยใช้ requests
"""

import sys
import json
import requests
from pathlib import Path
import time
import re

class YouTubeCommentScraperRequests:
    def __init__(self, output_dir="youtube_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def extract_video_id(self, url):
        """แยก video_id จาก URL YouTube"""
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_comments(self, video_id, max_comments=100):
        """ดึงความคิดเห็นโดยใช้ requests"""
        comments = []
        continuation_token = None

        # URL สำหรับดึงความคิดเห็น
        base_url = "https://www.youtube.com/youtubei/v1/next"

        # Payload สำหรับ API call แรก
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20210721.00.00"
                }
            },
            "continuation": continuation_token,
            "videoId": video_id
        }

        headers = {
            'Content-Type': 'application/json',
            'X-YouTube-Client-Name': '1',
            'X-YouTube-Client-Version': '2.20210721.00.00'
        }

        try:
            response = self.session.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            # แยกความคิดเห็นจาก response
            if 'contents' in data and 'twoColumnWatchNextResults' in data['contents']:
                results = data['contents']['twoColumnWatchNextResults']
                if 'results' in results and 'results' in results['results']:
                    contents = results['results']['results']['contents']

                    for content in contents:
                        if 'itemSectionRenderer' in content:
                            for item in content['itemSectionRenderer']['contents']:
                                if 'commentThreadRenderer' in item:
                                    comment_thread = item['commentThreadRenderer']
                                    comment_data = self._parse_comment(comment_thread)
                                    if comment_data:
                                        comments.append(comment_data)

                                        if len(comments) >= max_comments:
                                            break

                            if len(comments) >= max_comments:
                                break

        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดึงความคิดเห็น: {e}")
            return []

        return comments[:max_comments]

    def _parse_comment(self, comment_thread):
        """แยกข้อมูลความคิดเห็น"""
        try:
            comment = comment_thread['comment']['commentRenderer']

            author = comment['authorText']['simpleText']
            comment_text = comment['contentText']['runs'][0]['text'] if 'runs' in comment['contentText'] else comment['contentText']['simpleText']
            likes = comment.get('likeCount', 0)
            published_time = comment.get('publishedTimeText', {}).get('runs', [{}])[0].get('text', '')

            return {
                "author": author,
                "comment": comment_text,
                "likes": str(likes),
                "time": published_time
            }
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการแยกความคิดเห็น: {e}")
            return None

    def save_comments(self, comments, video_id, filename=None):
        """บันทึกความคิดเห็นเป็นไฟล์ JSONL"""
        if filename is None:
            filename = f"youtube_comments_{video_id}.jsonl"

        output_file = self.output_dir / filename

        with open(output_file, 'w', encoding='utf-8') as f:
            for comment in comments:
                json.dump(comment, f, ensure_ascii=False)
                f.write('\n')

        print(f"บันทึกความคิดเห็น {len(comments)} รายการไปยัง {output_file}")

    def scrape_video_comments(self, video_url, max_comments=100):
        """ฟังก์ชันหลักสำหรับดึงความคิดเห็น"""
        video_id = self.extract_video_id(video_url)
        if not video_id:
            print("ไม่สามารถแยก video_id จาก URL")
            return []

        print(f"กำลังดึงความคิดเห็นจากวิดีโอ: {video_id}")

        comments = self.get_comments(video_id, max_comments)
        if comments:
            self.save_comments(comments, video_id)

        return comments

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_comment_scraper_requests.py <video_url> [max_comments]")
        print("Example: python youtube_comment_scraper_requests.py https://www.youtube.com/watch?v=VIDEO_ID 50")
        sys.exit(1)

    video_url = sys.argv[1]
    max_comments = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    scraper = YouTubeCommentScraperRequests()
    scraper.scrape_video_comments(video_url, max_comments)

if __name__ == "__main__":
    main()
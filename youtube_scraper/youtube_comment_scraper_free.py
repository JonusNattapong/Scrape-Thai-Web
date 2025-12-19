#!/usr/bin/env python3
"""
YouTube Comment Scraper (Free Alternative)
ดึงความคิดเห็นจากวิดีโอ YouTube โดยใช้ scrapetube
"""

import sys
import json
from pathlib import Path
import scrapetube

class YouTubeCommentScraperFree:
    def __init__(self, output_dir="youtube_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def extract_video_id(self, url):
        """แยก video_id จาก URL YouTube"""
        import re
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

    def scrape_comments(self, video_url, max_comments=100):
        """ดึงความคิดเห็นโดยใช้ scrapetube"""
        video_id = self.extract_video_id(video_url)
        if not video_id:
            print("ไม่สามารถแยก video_id จาก URL")
            return []

        print(f"กำลังดึงความคิดเห็นจากวิดีโอ: {video_id}")

        comments = []
        try:
            # ใช้ scrapetube เพื่อดึงความคิดเห็น
            data = scrapetube.get_comments(video_id, limit=max_comments)

            for i, comment in enumerate(data):
                try:
                    # แปลงข้อมูลจาก scrapetube format
                    comment_data = {
                        "author": comment.get('author', {}).get('name', 'Unknown'),
                        "comment": comment.get('text', {}).get('runs', [{}])[0].get('text', ''),
                        "likes": str(comment.get('likeCount', 0)),
                        "time": comment.get('publishedTimeText', {}).get('runs', [{}])[0].get('text', ''),
                        "author_id": comment.get('author', {}).get('id', ''),
                        "is_hearted": comment.get('isHearted', False)
                    }

                    comments.append(comment_data)
                    print(f"ดึงความคิดเห็นที่ {i+1}: {comment_data['author']}")

                except Exception as e:
                    print(f"เกิดข้อผิดพลาดในการประมวลผลความคิดเห็นที่ {i+1}: {e}")
                    continue

        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดึงความคิดเห็น: {e}")
            return []

        return comments

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
        comments = self.scrape_comments(video_url, max_comments)
        if comments:
            video_id = self.extract_video_id(video_url)
            self.save_comments(comments, video_id)
        return comments

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_comment_scraper_free.py <video_url> [max_comments]")
        print("Example: python youtube_comment_scraper_free.py https://www.youtube.com/watch?v=VIDEO_ID 50")
        sys.exit(1)

    video_url = sys.argv[1]
    max_comments = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    scraper = YouTubeCommentScraperFree()
    scraper.scrape_video_comments(video_url, max_comments)

if __name__ == "__main__":
    main()
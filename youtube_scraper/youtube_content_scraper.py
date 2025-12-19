#!/usr/bin/env python3
"""
YouTube Content Scraper
ดึงเนื้อหาวิดีโอ (transcript/caption) จาก YouTube
"""

import sys
import json
import re
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter

class YouTubeContentScraper:
    def __init__(self, output_dir="youtube_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

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

    def get_transcript(self, video_id, language='th'):
        """ดึง transcript ของวิดีโอ"""
        languages_to_try = [language, 'th-TH', 'th', 'en', 'en-US']

        for lang in languages_to_try:
            try:
                print(f"ลองดึง transcript ภาษา {lang}...")
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                print(f"พบ transcript ภาษา {lang}")
                return transcript
            except Exception as e:
                print(f"ไม่พบ transcript ภาษา {lang}: {str(e)[:50]}...")
                continue

        # ลอง list และ fetch โดยตรง
        try:
            print("ลอง list transcripts...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            available_transcripts = list(transcript_list)
            print(f"พบ {len(available_transcripts)} transcripts")
            for t in available_transcripts:
                print(f"  - {t.language} (Generated: {t.is_generated})")
            if available_transcripts:
                transcript = available_transcripts[0].fetch()
                print(f"ดึง transcript ภาษา {available_transcripts[0].language}")
                return transcript
        except Exception as e3:
            print(f"ไม่สามารถ fetch transcript: {str(e3)[:50]}...")

        return None

    def clean_transcript_text(self, text):
        """ทำความสะอาดข้อความ transcript"""
        # ลบ timestamp และ formatting
        text = re.sub(r'\[\d+:\d+:\d+\.\d+\]', '', text)
        text = re.sub(r'\[\d+:\d+\]', '', text)

        # ลบ extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # ลบ special characters ที่ไม่ต้องการ
        text = re.sub(r'[^\w\s\u0E00-\u0E7F.,!?]', '', text)  # เก็บตัวอักษรไทย อังกฤษ และเครื่องหมายบางตัว

        return text

    def format_transcript(self, transcript, format_type='text'):
        """จัดรูปแบบ transcript"""
        if format_type == 'text':
            formatter = TextFormatter()
            return formatter.format_transcript(transcript)
        elif format_type == 'json':
            formatter = JSONFormatter()
            return formatter.format_transcript(transcript)
        else:
            return transcript

    def save_transcript(self, transcript, video_id, format_type='text', filename=None):
        """บันทึก transcript เป็นไฟล์"""
        if filename is None:
            filename = f"youtube_transcript_{video_id}.{format_type}"

        output_file = self.output_dir / filename

        formatted_transcript = self.format_transcript(transcript, format_type)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_transcript)

        print(f"บันทึก transcript ไปยัง {output_file}")

        # สร้างไฟล์ JSONL สำหรับข้อมูลที่มีโครงสร้าง
        jsonl_file = self.output_dir / f"youtube_content_{video_id}.jsonl"
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for entry in transcript:
                content_data = {
                    "start": entry['start'],
                    "duration": entry['duration'],
                    "text": self.clean_transcript_text(entry['text'])
                }
                json.dump(content_data, f, ensure_ascii=False)
                f.write('\n')

        print(f"บันทึกเนื้อหาเป็น JSONL ไปยัง {jsonl_file}")

    def scrape_video_content(self, video_url, language='th'):
        """ฟังก์ชันหลักสำหรับดึงเนื้อหาวิดีโอ"""
        video_id = self.extract_video_id(video_url)
        if not video_id:
            print("ไม่สามารถแยก video_id จาก URL")
            return None

        print(f"กำลังดึงเนื้อหาวิดีโอ: {video_id}")

        transcript = self.get_transcript(video_id, language)
        if transcript:
            self.save_transcript(transcript, video_id)
            return transcript
        else:
            print("ไม่สามารถดึง transcript")
            return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_content_scraper.py <video_url> [language]")
        print("Example: python youtube_content_scraper.py https://www.youtube.com/watch?v=VIDEO_ID th")
        print("Languages: th (Thai), en (English), etc.")
        sys.exit(1)

    video_url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'th'

    scraper = YouTubeContentScraper()
    scraper.scrape_video_content(video_url, language)

if __name__ == "__main__":
    main()
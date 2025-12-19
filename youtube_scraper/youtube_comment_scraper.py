#!/usr/bin/env python3
"""
YouTube Comment Scraper
ดึงความคิดเห็นจากวิดีโอ YouTube
"""

import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

class YouTubeCommentScraper:
    def __init__(self, output_dir="youtube_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.driver = None

    def setup_driver(self):
        """ตั้งค่า WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in background
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.page_load_strategy = 'eager'  # Faster loading

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            print("WebDriver เริ่มทำงานแล้ว")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการตั้งค่า WebDriver: {e}")
            sys.exit(1)

    def scroll_to_load_comments(self, max_scrolls=10):
        """เลื่อนหน้าเพื่อโหลดความคิดเห็นเพิ่มเติม"""
        for i in range(max_scrolls):
            try:
                # เลื่อนไปยังส่วนความคิดเห็น
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # คลิก "แสดงเพิ่มเติม" ถ้ามี
                try:
                    show_more_buttons = self.driver.find_elements(By.XPATH, "//yt-formatted-string[@class='more-button style-scope ytd-comment-renderer']")
                    for button in show_more_buttons:
                        if button.is_displayed():
                            button.click()
                            time.sleep(1)
                except:
                    pass

                print(f"เลื่อนครั้งที่ {i+1}")
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการเลื่อน: {e}")
                break

    def extract_comments(self, video_url, max_comments=100):
        """ดึงความคิดเห็นจาก URL วิดีโอ"""
        try:
            print(f"กำลังดึงความคิดเห็นจาก: {video_url}")
            self.driver.get(video_url)
            time.sleep(5)  # รอให้หน้าโหลด

            # ยอมรับคุกกี้ถ้ามี
            try:
                accept_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Accept') or contains(text(), 'Accept')]"))
                )
                accept_button.click()
                time.sleep(2)
            except:
                pass

            # เลื่อนเพื่อโหลดความคิดเห็น
            self.scroll_to_load_comments()

            comments = []
            comment_elements = self.driver.find_elements(By.XPATH, "//ytd-comment-thread-renderer")

            for i, comment_elem in enumerate(comment_elements[:max_comments]):
                try:
                    # ชื่อผู้แสดงความคิดเห็น
                    author_elem = comment_elem.find_element(By.XPATH, ".//a[@id='author-text']")
                    author = author_elem.text.strip()

                    # ความคิดเห็น
                    comment_elem_text = comment_elem.find_element(By.XPATH, ".//yt-formatted-string[@id='content-text']")
                    comment_text = comment_elem_text.text.strip()

                    # จำนวนไลค์
                    try:
                        likes_elem = comment_elem.find_element(By.XPATH, ".//span[@id='vote-count-middle']")
                        likes = likes_elem.text.strip()
                    except:
                        likes = "0"

                    # เวลาที่โพสต์
                    try:
                        time_elem = comment_elem.find_element(By.XPATH, ".//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
                        post_time = time_elem.text.strip()
                    except:
                        post_time = ""

                    comment_data = {
                        "author": author,
                        "comment": comment_text,
                        "likes": likes,
                        "time": post_time
                    }

                    comments.append(comment_data)
                    print(f"ดึงความคิดเห็นที่ {i+1}: {author}")

                except Exception as e:
                    print(f"เกิดข้อผิดพลาดในการดึงความคิดเห็นที่ {i+1}: {e}")
                    continue

            return comments

        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดึงความคิดเห็น: {e}")
            return []

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
        if not self.driver:
            self.setup_driver()

        # แยก video_id จาก URL
        if 'v=' in video_url:
            video_id = video_url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in video_url:
            video_id = video_url.split('youtu.be/')[1].split('?')[0]
        else:
            print("URL ไม่ถูกต้อง")
            return

        comments = self.extract_comments(video_url, max_comments)
        self.save_comments(comments, video_id)

        return comments

    def close(self):
        """ปิด WebDriver"""
        if self.driver:
            self.driver.quit()
            print("WebDriver ปิดแล้ว")

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_comment_scraper.py <video_url> [max_comments]")
        print("Example: python youtube_comment_scraper.py https://www.youtube.com/watch?v=VIDEO_ID 50")
        sys.exit(1)

    video_url = sys.argv[1]
    max_comments = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    scraper = YouTubeCommentScraper()
    try:
        scraper.scrape_video_comments(video_url, max_comments)
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
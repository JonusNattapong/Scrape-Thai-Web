# YouTube Scraper

This directory contains scripts to scrape YouTube video comments and content (transcripts/captions) in Thai.

## Files

- `youtube_comment_scraper.py`: Scrapes comments from YouTube videos using Selenium
- `youtube_content_scraper.py`: Downloads video transcripts/captions using YouTube API
- `requirements.txt`: Python dependencies
- `install_deps.bat`: Batch file to install dependencies
- `run_comment_scraper.bat`: Batch file to run comment scraper
- `run_content_scraper.bat`: Batch file to run content scraper

## Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

Or use the batch file:
```
install_deps.bat
```

## Usage

### Scraping Comments

Run the comment scraper:
```bash
python youtube_comment_scraper.py <video_url> [max_comments]
```

Example:
```bash
python youtube_comment_scraper.py https://www.youtube.com/watch?v=dQw4w9WgXcQ 50
```

Or use the batch file:
```
run_comment_scraper.bat
```

This will:
- Open a headless Chrome browser
- Load the YouTube video
- Scroll to load comments
- Extract up to max_comments (default 100)
- Save to `youtube_data/youtube_comments_{video_id}.jsonl`

### Scraping Video Content (Transcripts)

Run the content scraper:
```bash
python youtube_content_scraper.py <video_url> [language]
```

Example:
```bash
python youtube_content_scraper.py https://www.youtube.com/watch?v=dQw4w9WgXcQ th
```

Or use the batch file:
```
run_content_scraper.bat
```

This will:
- Extract video ID from URL
- Download transcript in specified language (default: Thai)
- Save formatted text to `youtube_data/youtube_transcript_{video_id}.txt`
- Save structured data to `youtube_data/youtube_content_{video_id}.jsonl`

## Data Format

### Comments (JSONL)
Each line is a JSON object:
```json
{
  "author": "Username",
  "comment": "Comment text",
  "likes": "42",
  "time": "2 days ago"
}
```

### Content (JSONL)
Each line is a JSON object:
```json
{
  "start": 10.5,
  "duration": 5.2,
  "text": "Cleaned transcript text"
}
```

## Requirements

- Chrome browser installed
- Internet connection
- For comments: Selenium WebDriver (auto-installed)
- For transcripts: Video must have captions/transcripts available

## Notes

- Respect YouTube's Terms of Service
- Comment scraping may be slow due to page loading
- Not all videos have transcripts available
- Transcripts are downloaded in preferred language, fallback to English or any available
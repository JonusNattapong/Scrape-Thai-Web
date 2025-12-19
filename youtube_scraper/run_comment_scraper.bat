@echo off
echo YouTube Comment Scraper
echo =======================
set /p video_url="Enter YouTube video URL: "
set /p max_comments="Enter max comments to scrape (default 100): "
if "%max_comments%"=="" set max_comments=100

echo Running comment scraper for %video_url% (max %max_comments% comments)...
python youtube_comment_scraper.py "%video_url%" %max_comments%
echo Scraper finished.
pause
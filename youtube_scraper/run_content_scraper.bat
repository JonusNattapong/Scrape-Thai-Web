@echo off
echo YouTube Content Scraper
echo =======================
set /p video_url="Enter YouTube video URL: "
set /p language="Enter language code (default th for Thai): "
if "%language%"=="" set language=th

echo Running content scraper for %video_url% (language %language%)...
python youtube_content_scraper.py "%video_url%" %language%
echo Scraper finished.
pause
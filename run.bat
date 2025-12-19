@echo off
echo Scrape-Thai-Web Easy Runner
echo ===========================
echo 1. Run Pantip Scraper
echo 2. Run Wikipedia Processor
echo 3. Run YouTube Comment Scraper
echo 4. Run YouTube Content Scraper
echo 5. Install Dependencies for Pantip
echo 6. Install Dependencies for Wikipedia
echo 7. Install Dependencies for YouTube
echo 8. Exit
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    cd pantip_scraper
    call run_scraper.bat
) else if "%choice%"=="2" (
    cd wikipedia_scraper
    call run_processor.bat
) else if "%choice%"=="3" (
    cd youtube_scraper
    call run_comment_scraper.bat
) else if "%choice%"=="4" (
    cd youtube_scraper
    call run_content_scraper.bat
) else if "%choice%"=="5" (
    cd pantip_scraper
    call install_deps.bat
) else if "%choice%"=="6" (
    cd wikipedia_scraper
    call install_deps.bat
) else if "%choice%"=="7" (
    cd youtube_scraper
    call install_deps.bat
) else if "%choice%"=="8" (
    echo Exiting...
    exit /b
) else (
    echo Invalid choice. Please run again.
)

pause
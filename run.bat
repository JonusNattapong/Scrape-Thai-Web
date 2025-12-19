@echo off
echo Scrape-Thai-Web Easy Runner
echo ===========================
echo 1. Run Pantip Scraper
echo 2. Run Wikipedia Processor
echo 3. Install Dependencies for Pantip
echo 4. Install Dependencies for Wikipedia
echo 5. Exit
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    cd pantip_scraper
    call run_scraper.bat
) else if "%choice%"=="2" (
    cd wikipedia_scraper
    call run_processor.bat
) else if "%choice%"=="3" (
    cd pantip_scraper
    call install_deps.bat
) else if "%choice%"=="4" (
    cd wikipedia_scraper
    call install_deps.bat
) else if "%choice%"=="5" (
    echo Exiting...
    exit /b
) else (
    echo Invalid choice. Please run again.
)

pause
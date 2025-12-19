# Scrape-Thai-Web

A project to scrape Thai websites for clean text data, including Pantip forum posts and Thai Wikipedia articles. The data is cleaned and formatted for use in NLP tasks or text analysis.

## Project Structure

- `pantip_scraper/`: Directory for scraping Pantip forum data
  - `pantip_scraper.py`: Scraper for Pantip.com forum posts
  - `check_data.py`: Script to verify extracted data
  - `requirements.txt`: Python dependencies
  - `list.txt`: List of Pantip topic URLs to scrape
  - `data/pantip_dataset.jsonl`: Extracted Pantip data
  - `install_deps.bat`: Batch file to install dependencies
  - `run_scraper.bat`: Batch file to run the scraper

- `wikipedia_scraper/`: Directory for processing Thai Wikipedia dump
  - `wiki_processor.py`: Downloads, processes, and cleans Thai Wikipedia articles
  - `data/wiki_dataset_clean.jsonl`: Cleaned Thai Wikipedia articles
  - `requirements.txt`: Python dependencies
  - `install_deps.bat`: Batch file to install dependencies
  - `run_processor.bat`: Batch file to run the processor

- `run.bat`: Main batch file for interactive menu to run scrapers or install dependencies

## Installation

1. Install dependencies for each scraper:
   ```bash
   cd pantip_scraper
   pip install -r requirements.txt

   cd ../wikipedia_scraper
   pip install -r requirements.txt
   ```

   Or use the provided batch files:
   - `pantip_scraper/install_deps.bat`
   - `wikipedia_scraper/install_deps.bat`

## Usage

Use the main runner script: `run.bat` for an interactive menu to run scrapers or install dependencies.

### Manual Usage

#### Scraping Pantip Data

1. Add Pantip topic URLs to `pantip_scraper/list.txt` (one per line).
2. Run the scraper:
   ```bash
   cd pantip_scraper
   python pantip_scraper.py
   ```
   Or use: `pantip_scraper/run_scraper.bat`
3. Data will be saved to `pantip_scraper/data/pantip_dataset.jsonl`.

#### Processing Thai Wikipedia Dump

1. Run the wiki processor:
   ```bash
   cd wikipedia_scraper
   python wiki_processor.py
   ```
   Or use: `wikipedia_scraper/run_processor.bat`
2. This will download the latest Thai Wikipedia dump, extract and clean articles, saving to `wikipedia_scraper/data/wiki_dataset_clean.jsonl`.

### Checking Data

- To check Pantip data: `cd pantip_scraper && python check_data.py`

## Data Format

Both datasets are in JSONL format, with each line being a JSON object.

- Pantip: `{"topic_id": "...", "title": "...", "summary": "...", "comments": ["...", "..."]}`
- Wiki: `{"title": "...", "content": "..."}`

## Notes

- Respect website terms of service and robots.txt when scraping.
- Wikipedia dump downloads are large (~1GB compressed); ensure sufficient disk space.
- Data is cleaned to remove HTML, wiki markup, and other artifacts for clean text analysis.


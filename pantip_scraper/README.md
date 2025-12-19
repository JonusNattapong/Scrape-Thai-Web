# Pantip Scraper

This directory contains scripts to scrape data from Pantip.com, a popular Thai web forum.

## Files

- `pantip_scraper.py`: Main scraper script that collects forum posts and comments.
- `check_data.py`: Script to analyze and check the scraped data.
- `list.txt`: List of URLs or topics to scrape.
- `requirements.txt`: Python dependencies required for the scraper.
- `data/pantip_dataset.jsonl`: Output file containing scraped data in JSONL format.

## Installation

1. Install Python 3.7+ if not already installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Scraping Data

Run the main scraper:

```
python pantip_scraper.py
```

This will scrape forum data based on the URLs in `list.txt` and save to `data/pantip_dataset.jsonl`.

### Checking Data

To analyze the scraped data:

```
python check_data.py
```

This will provide statistics and insights about the collected data.

## Data Format

The output is in JSONL format, with each line being a JSON object containing:
- `title`: Post title
- `content`: Post content
- `author`: Author name
- `date`: Post date
- `comments`: List of comment objects

## Notes

- Respect Pantip's terms of service and robots.txt.
- Use responsibly to avoid overloading the server.
- The scraper may need updates if Pantip changes their website structure.
# Wikipedia Scraper

This directory contains scripts to download and process the Thai Wikipedia dump for extracting article data.

## Files

- `wiki_processor.py`: Main script that downloads the Thai Wikipedia dump and extracts articles.
- `wikipedia_dump_scraper.py`: Additional scraper for specific Wikipedia pages if needed.
- `requirements.txt`: Python dependencies required.
- `thwiki-latest-pages-articles.xml.bz2`: Downloaded Wikipedia dump file (large, ~1GB).
- `data/wiki_dataset_clean.jsonl`: Output file with cleaned article data.

## Installation

1. Install Python 3.7+ if not already installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Processing Wikipedia Dump

Run the processor to download and extract articles:

```
python wiki_processor.py
```

This will:
1. Download the latest Thai Wikipedia dump (if not present).
2. Parse the XML dump.
3. Extract article titles and cleaned content.
4. Save 1000 articles to `data/wiki_dataset_clean.jsonl`.

The processing may take several minutes due to the large dump size.

### Data Format

Output is in JSONL format, each line a JSON object:
- `title`: Article title
- `content`: Cleaned article text (wiki markup removed, HTML stripped, etc.)

## Notes

- The dump file is large (~1GB compressed). Ensure sufficient disk space.
- Processing requires significant memory and time.
- The script uses mwparserfromhell for wiki markup parsing and additional regex cleaning.
- Articles are filtered to main namespace, excluding templates, categories, etc.
- Content is limited to 10,000 characters per article.
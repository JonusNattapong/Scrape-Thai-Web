import requests
import json
import os
import bz2
import xml.etree.ElementTree as ET
from mwparserfromhell import parse
import re

def clean_wiki_text(text):
    """Clean wiki markup text to plain text with additional cleaning."""
    if not text:
        return ""
    # Parse wiki markup
    wikicode = parse(text)
    # Remove templates, links, etc., keep plain text
    plain = wikicode.strip_code()
    
    # Additional cleaning from clean_all.py
    # Remove all "()"
    plain = re.sub(r'\(\)', '', plain)
    # Remove HTML tags
    plain = re.sub(r'<[^>]+>', '', plain)
    # Remove wiki markup like thumb|, alt=, etc.
    plain = re.sub(r'thumb\|[^|]*\|', '', plain)
    plain = re.sub(r'alt=[^|]*\|', '', plain)
    plain = re.sub(r'right\|', '', plain)
    plain = re.sub(r'upright=[^|]*\|', '', plain)
    # Remove other wiki links and templates (already done by mwparserfromhell, but ensure)
    plain = re.sub(r'\[\[.*?\]\]', '', plain)
    plain = re.sub(r'\{\{.*?\}\}', '', plain)
    # Remove references [1], [2], etc.
    plain = re.sub(r'\[\d+\]', '', plain)
    
    # Additional patterns
    additional_patterns = [
        r'\(; , \)',
        r'\(, \)',
        r'thumb\|',
        r'\(; \)',
        r'frameless\|350px',
        r'250px\|',
        r'thumbnail\|300px\|',
        r'\(; ; \)'
    ]
    for pattern in additional_patterns:
        plain = re.sub(pattern, '', plain)
    
    # Clean up whitespace
    plain = re.sub(r'\s+', ' ', plain)
    return plain.strip()

def download_wiki_dump(url, output_path):
    """Download the wiki dump file."""
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {output_path}")

def process_wiki_dump(dump_path, output_file, max_articles=1000):
    """Process the wiki dump and extract articles."""
    print(f"Processing {dump_path}...")
    articles = []
    ns = {'mw': 'http://www.mediawiki.org/xml/export-0.11/'}
    
    with bz2.open(dump_path, 'rt', encoding='utf-8') as f:
        # Parse XML
        context = ET.iterparse(f, events=('end',))
        for event, elem in context:
            if elem.tag == f"{{{ns['mw']}}}page":
                title_elem = elem.find('mw:title', ns)
                ns_elem = elem.find('mw:ns', ns)
                revision = elem.find('mw:revision', ns)
                if title_elem is not None and ns_elem is not None and revision is not None:
                    title_text = title_elem.text
                    ns_text = ns_elem.text
                    text_elem = revision.find('mw:text', ns)
                    if text_elem is not None and ns_text == '0':  # main namespace
                        content_text = text_elem.text
                        if content_text and not title_text.startswith('วิกิพีเดีย:') and not title_text.startswith('แม่แบบ:') and not title_text.startswith('หมวดหมู่:'):
                            clean_content = clean_wiki_text(content_text)
                            if clean_content and len(clean_content) > 100:  # minimum length
                                article = {
                                    'title': title_text,
                                    'content': clean_content[:10000]  # Limit content length
                                }
                                articles.append(article)
                                print(f"Extracted: {title_text}")
                                if len(articles) >= max_articles:
                                    break
                elem.clear()
    # Save to JSONL
    with open(output_file, 'w', encoding='utf-8') as f:
        for article in articles:
            f.write(json.dumps(article, ensure_ascii=False) + '\n')
    print(f"Saved {len(articles)} articles to {output_file}")

if __name__ == "__main__":
    # URL for Thai Wikipedia dump (latest articles)
    dump_url = "https://dumps.wikimedia.org/thwiki/latest/thwiki-latest-pages-articles.xml.bz2"
    dump_path = "thwiki-latest-pages-articles.xml.bz2"
    output_file = "data/wiki_dataset_clean.jsonl"

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Download dump
    if not os.path.exists(dump_path):
        download_wiki_dump(dump_url, dump_path)
    else:
        print(f"Dump already exists: {dump_path}")

    # Process dump
    process_wiki_dump(dump_path, output_file)
#!/usr/bin/env python3

import sys
import json
import argparse
import re
import urllib.request
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

#HOST = 'kolekcje.lan'
HOST = '192.168.0.119'
PORT = '5000'

def fetch_api_data(host, port, field, name):
    """
    Sends a GET request to the backend to check if the entity exists.
    """

    replacements = { "komiksy": "komiks" }

    qtype = field
    if not qtype.endswith('s'):
        qtype += 's'
    url = f"http://{host}:{port}/{qtype}?query={urllib.parse.quote(name)}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for val in data:
                    if 'id' in val:
                        if val['id'] is not None:
                            if name in replacements:
                                name = replacements[name]
                            return {"id": val['id'], "title": name, "isCustom": False}
    except Exception as e:
        # Catch network errors, 404s, etc. and fall back to isCustom = True
        pass

    return {"id": None, "title": name, "isCustom": True}

def extract_year(value):
    """
    Extracts the first 4 digits from a string to represent the year.
    """
    if not value:
        return None
    match = re.search(r'\d{4}', str(value))
    return int(match.group(0)) if match else None

def parse_book_html(html_content, host, port):
    """
    Parses HTML, formats keys, maps API fields, and returns the final dictionary.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    container = soup.find('section', class_='container book', id='container-book')

    if not container:
        raise ValueError("Main container not found in HTML.")

    def get_class_values(class_name):
        elements = container.find_all(class_=class_name)
        if not elements:
            return None
        texts = [el.get_text(strip=True) for el in elements]
        return texts if len(texts) > 1 else texts[0]

    # 1. Gather raw data from the HTML
    raw_data = {}

    raw_data['book_title'] = get_class_values('book__title')
    raw_data['author'] = get_class_values('author')

    if 'author' in raw_data:
        raw_data['author'] = raw_data['author'].split(',')

    def getPublisher(soup):
        if soup:
            section = soup.find('section', id = 'container-book' )
            if section:
                publisher = section.get('data-ga-book-publishers')
                if publisher:
                    return publisher.split(',')

        return None

    publisher = getPublisher(soup)
    if publisher:
        raw_data['publisher'] = publisher

    details_container = container.find(id='book-details')
    if details_container:
        dts = details_container.find_all('dt')
        dds = details_container.find_all('dd')
        for dt, dd in zip(dts, dds):
            key = dt.get_text(strip=True)
            if key.endswith(':'):
                key = key[:-1].strip()
            value = dd.get_text(strip=True)

            if key in raw_data:
                if isinstance(raw_data[key], list):
                    raw_data[key].append(value)
                else:
                    raw_data[key] = [raw_data[key], value]
            else:
                raw_data[key] = value

    # 2. Map raw data to the output schema and process values
    output = {}

    # Title is mandatory
    if not raw_data.get('book_title'):
        raise ValueError("Mandatory field 'book_title' (title) was not found.")

    # Ensure title is a string, not a list
    output['title'] = raw_data['book_title'][0] if isinstance(raw_data['book_title'], list) else raw_data['book_title']

    # Simple field mappings
    simple_mappings = {
        'Tytuł oryginału': 'originalTitle',
        'Liczba stron': 'pages',
        'Język': 'language',
        'ISBN': 'isbn',
        'Tłumacz': 'translator'
    }

    for pl_key, eng_key in simple_mappings.items():
        if pl_key in raw_data:
            val = raw_data[pl_key]
            # Convert numeric fields to integers
            if eng_key in ['pages', 'isbn']:
                try:
                    val = int(re.sub(r'\D', '', str(val)))
                except ValueError:
                    pass
            output[eng_key] = val

    # Year fields mapping
    if 'Data wydania' in raw_data:
        yr = extract_year(raw_data['Data wydania'])
        if yr: output['publishYear'] = yr

    if 'Data 1. wyd. pol.' in raw_data:
        yr = extract_year(raw_data['Data 1. wyd. pol.'])
        if yr: output['firstPublishYear'] = yr

    # Complex fields needing API lookups
    api_mappings = {
        'author': 'author',
        'publisher': 'publisher',
        'Kategoria': 'genre',
        'Seria': 'series'
    }

    for pl_key, api_field in api_mappings.items():
        if pl_key in raw_data:
            raw_val = raw_data[pl_key]
            val_list = raw_val if isinstance(raw_val, list) else [raw_val]

            api_results = []
            for item in val_list:
                api_results.append(fetch_api_data(host, port, api_field, item))

            # If there's multiple items, save as list. If single, keep as object unless you want strictly lists for everything.
            if len(api_results) > 1 or api_field in ['author', 'genre', 'publisher']:
                output[api_field] = api_results
            else:
                output[api_field] = api_results[0]

    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse book HTML and fetch missing taxonomy IDs via API.")
    parser.add_argument("filename", help="Path to the HTML file to parse")
    args = parser.parse_args()

    input_path = Path(args.filename)
    if not input_path.is_file():
        print(f"Error: File '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Read HTML content
    with open(input_path, "r", encoding="utf-8") as f:
        html_data = f.read()

    try:
        # Parse and fetch data
        parsed_data = parse_book_html(html_data, HOST, PORT )
    except ValueError as e:
        print(f"Parsing error: {e}", file=sys.stderr)
        sys.exit(1)

    # Save output to a JSON file with the same base name
    output_path = input_path.with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=3, ensure_ascii=False)

    print(f"Successfully saved parsed JSON to: {output_path}")

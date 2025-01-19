from urllib.parse import urlparse, unquote
import logging

def get_basename_from_uri(uri):
    # Parse the URI
    parsed = urlparse(uri)

    # Get the path and decode URL-encoded characters
    path = unquote(parsed.path)

    # Handle trailing slash
    path = path.rstrip('/')

    # If path is empty, try to use the netloc (domain)
    if not path:
        return parsed.netloc

    # Get the last part of the path
    basename = path.split('/')[-1]

    return basename

def transform_name(text: str) -> str:
    if not text:
        return ""

    # Handle case with no hyphens
    if '-' not in text:
        return text[0].upper() + text[1:]

    # Split by hyphen and filter out empty strings
    words = [word for word in text.split('-') if word]

    # Handle empty result after splitting
    if not words:
        return ""

    # Capitalize each word and join
    return ''.join(word.capitalize() for word in words)


def translate_keys(data: dict) -> dict:

    # Define translation mapping
    key_mapping = {
        "ISBN": "isbn",
        "Tytuł": "title",
        "Autor": "author",
        "Data wydania": "publishYear",
        "Data 1. wydania": "firstPublishYear",
        "Data 1. wyd. pol.": "firstPublishYear",
        "Format": "format",
        "Wydawnictwo": "publisher",
        "Liczba stron": "pages",
        "Opis": "description",
        "Seria": "series",
        "Tytuł oryginału": "originalTitle",
        "Tłumacz": "translator",
        "Kategoria": "genre",
        "Język": "language"
    }

    # Create new dictionary with translated keys
    translated_data = {}

    for key, value in data.items():
        if key in key_mapping:
            if key == "Data 1. wydania" or key == "Data 1. wyd. pol.":
                if "firstPublishYear" in translated_data:
                    logging.warning( f"{podwojony element pierwszego wydania" )
                    continue
            translated_data[key_mapping[key]] = value
        else:
            logging.warning(f"Removing unspecified key: '{key}' with value: '{value}'")

    if "publishYear" in translated_data:
        year = int( translated_data["publishYear"].split('-')[0] )

    if "firstPublishYear" in translated_data:
        year = int( translated_data["firstPublishYear"].split('-')[0] )

    return translated_data

import json
import jsonschema
from jsonschema import validate

def load_json_schema(schema_path):
    """Load JSON Schema from a file."""
    try:
        with open(schema_path, 'r') as schema_file:
            return json.load(schema_file)
    except FileNotFoundError:
        raise Exception(f"Schema file not found: {schema_path}")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON in schema file: {schema_path}")

def validate_book_json(json_data, schema_path="schemaBookNew.json"):
    """Validate JSON data against the schema."""
    try:
        schema = load_json_schema(schema_path)
        validate(instance=json_data, schema=schema)
        print("Validation successful! The JSON data is valid according to the schema.")
        return True
    except jsonschema.exceptions.ValidationError as ve:
        print(f"Validation error: {ve.message}")
        return False
    except jsonschema.exceptions.SchemaError as se:
        print(f"Schema error: {se.message}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    # Example book data
    sample_book = {
        "isbn": 1234567890,
        "title": "Sample Book",
        "author": "John Doe",
        "publishYear": 2023,
        "firstPublishYear": 2023,
        "format": "paperback",
        "pages": 200,
        "description": "A sample book description",
        "notes": "Some notes about the book",
        "series": "Sample Series",
        "originalTitle": "Original Sample Book",
        "translator": "Jane Smith",
        "language": "eng"
    }

    # Validate the sample book
    validate_book_json(sample_book)

    # You can also test with invalid data
    invalid_book = {
        "isbn": "not-a-number",  # Invalid ISBN
        "format": "invalid-format"  # Invalid format
    }

    print("\nTesting invalid data:")
    validate_book_json(invalid_book)

# Example usage
if __name__ == "__main__":
    # Example book data
    sample_book = {
        "isbn": 1234567890,
        "title": "Sample Book",
        "author": "John Doe",
        "publishYear": 2023,
        "firstPublishYear": 2023,
        "format": "paperback",
        "pages": 200,
        "description": "A sample book description",
        "notes": "Some notes about the book",
        "series": "Sample Series",
        "originalTitle": "Original Sample Book",
        "translator": "Jane Smith",
        "language": "eng"
    }

    # Validate the sample book
    validate_book_json(sample_book)

    # You can also test with invalid data
    invalid_book = {
        "isbn": "not-a-number",  # Invalid ISBN
        "format": "invalid-format"  # Invalid format
    }

    print("\nTesting iexternal JSON:")
    validate_book_json(invalid_book)

    try:
        with open("book.json", 'r') as schema_file:
            book = json.load(schema_file)
            validate_book_json(book)
    except FileNotFoundError:
        raise Exception(f"Schema file not found: {schema_path}")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON in schema file: {schema_path}")

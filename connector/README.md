# connector

The `connector` package is the backend REST API for the book catalog. It is a
Flask application that exposes endpoints for querying, adding, updating and
validating books, as well as managing related entities such as authors,
publishers, series, genres and labels. It talks to a MariaDB database.

## Directory layout

```
connector/
├── Dockerfile          # Builds the production image
├── openapi.yaml        # OpenAPI specification of the API
├── Pipfile             # Pipenv dependency manifest
├── pytest.ini          # Pytest configuration
├── requirements.txt    # pip dependency list (used by the Docker image)
├── bookApp/            # The Flask application package
│   ├── source/         #   application implementation modules
│   └── tests/          #   unit tests
├── scripts/            # Standalone helper / one-off scripts
└── TestData/           # JSON data files used by the app and tests
```

## Running the application

### Locally (development)

The application is a Python package. From the `connector` directory, install
dependencies with Pipenv and start the Flask development server:

```bash
cd connector
pipenv install
pipenv run flask --app bookApp.source.app run --debug --host=0.0.0.0
```

The app listens on port `5000` by default. It expects a MariaDB database
reachable at host `db` (see `DB_CONFIG` in `bookApp/source/app.py`).

### Via Docker Compose

The repository provides several Compose files. The development one
(`compose_test.yml`) runs the app with the Flask dev server:

```bash
docker compose -f compose_test.yml up --build
```

The app is then available at `http://localhost:5000`.

## Building and using the Docker image

The `Dockerfile` installs the pip dependencies from `requirements.txt`, copies
the `bookApp`, `scripts` and `TestData` directories into the image, and starts
the app with gunicorn:

```bash
# Build the image
docker build -t katalog-connector ./connector

# Run it (gunicorn serves bookApp.source.app on port 5000)
docker run -p 5000:5000 katalog-connector
```

The gunicorn entrypoint is:

```
gunicorn --workers 4 --bind 0.0.0.0:5000 bookApp.source.app:app
```

The Compose files (`compose.yml`, `compose-deploy.yaml`, `compose-moode.yml`)
use this image and override the entrypoint with their own gunicorn settings.

## Running unit tests

Tests live inside the `bookApp/tests` package and are run with pytest. From the
`connector` directory:

```bash
cd connector
pipenv run pytest
```

To run a single test file:

```bash
pipenv run pytest bookApp/tests/test_isbn.py
```

There are 119 tests covering the API endpoints (authors, publishers, series,
genres, labels), book insertion, the query builder and ISBN validation. The
tests use mocked database connections, so no live database is required.

## The `bookApp` package

`bookApp` is the internal package that contains the Flask application. It is
split into two subpackages:

- `bookApp/source/` — the application implementation modules.
- `bookApp/tests/` — the unit tests.

### `bookApp/source`

- `app.py` — the Flask application. Defines the `app` object and all routes:
  `/keepalive`, `/book`, `/addbook`, `/authors`, `/publishers`, `/series`,
  `/genres`, `/labels`, `/series/add`, `/publisher/add`, `/bookinfo`,
  `/books/validate`, `/books/<id>` (GET/PUT/DELETE) and `/restart-router`.
  It also wires up the database connection and the handlers below.
- `addBook.py` — `BookDatabase`: inserts books into the database, including
  creating/attaching publishers, series, authors, labels and genres, and
  validating book data against a JSON schema.
- `updateBook.py` — `BookUpdateDatabase`: updates and deletes existing books.
- `bookinfo_handler.py` — `BookInfoHandler`: retrieves detailed book
  information based on dynamic search criteria.
- `table_handler.py` — `TableHandler`: generic CRUD helper for simple lookup
  tables (publisher, authors, series, genres, labels).
- `book_query_builder.py` — `BookQueryBuilder`: builds parameterized SQL
  queries for the `/book` endpoint from requested fields and filters.
- `isbn.py` — ISBN utilities: `validate_isbn`, `normalize_isbn`,
  `isbn10_to_isbn13` and `isbn2Book`.

### `bookApp/tests`

- `test_*.py` — unit tests for the modules in `bookApp/source`.

## The `scripts` directory

`scripts/` contains standalone helper and one-off scripts that are not part of
the Flask application:

- `askDuck.py` — searches DuckDuckGo for a book by ISBN.
- `findLangs.py` — scrapes Wiktionary for language codes.
- `goodreads.py` — scrapes Goodreads book data.
- `ib.py` — helpers for loading book data and making a database connection.
- `insertBook.py` — inserts a book from `output.json`.
- `insertGenres.py` — inserts genres into the database.
- `keys.py` — a set of book metadata field names.
- `mariadb_intro.py` — example of connecting to MariaDB.
- `nameUtils.py` — URI/basename helpers.
- `parseLC.py` — parses LubimyCzytac book pages.
- `populateBooks.py` — populates the database with random sample books.
- `queries.py` — database query helpers.
- `seriaLC.py` — scrapes a LubimyCzytac series page.
- `step_next.py` — step-by-step data migration helper.
- `translate.py` — translates/transforms `output.json` into `o2.json`.
- `validateNewBook.py` — validates book JSON against a JSON schema.

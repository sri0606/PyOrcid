# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyOrcid is a Python library and API client for interacting with the ORCID API. ORCID (Open Researcher and Contributor ID) provides unique identifiers to researchers. This library enables developers to access and manage ORCID profile data, including publications, employment, education, and other research activities.

## Development Commands

### Package Management
The project uses Poetry for dependency management:
```bash
# Install dependencies
poetry install

# Add a dependency
poetry add <package-name>

# Add a dev dependency
poetry add --group dev <package-name>
```

### Testing
```bash
# Run all tests
python -m unittest tests/test_orcid.py

# Run tests with pytest (if installed)
pytest tests/

# Run a single test
python -m unittest tests.test_orcid.TestOrcid.test_access_token_valid
```

### Linting
```bash
# Check for Python syntax errors and undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Full linting with warnings
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Building
```bash
# Build the package using Poetry
poetry build
```

## Architecture

### Core Classes

The library is organized into four main classes in `src/pyorcid/`:

1. **`Orcid` (orcid.py)** - The main API wrapper class
   - Handles both Public and Member API access
   - Requires an ORCID ID and access token
   - Supports sandbox mode for testing
   - Methods map to ORCID API v3.0 endpoints (e.g., `/works`, `/person`, `/educations`)
   - Returns tuples: `(processed_data, raw_api_response)` for most section methods
   - Key methods: `record()`, `works()`, `educations()`, `employments()`, `fundings()`, `person()`
   - Helper: `generate_markdown_file()` creates formatted reports

2. **`OrcidAuthentication` (orcid_authentication.py)** - Handles OAuth 2.0 authentication
   - `get_public_access_token()` - For reading public data (/read-public scope), no user auth required
   - `get_private_access_token()` - For Member API or limited-access data, requires user authorization
   - Supports both production and sandbox environments
   - Manages redirect URIs and authorization codes

3. **`OrcidScrapper` (orcid_scrapper.py)** - Alternative data access via web scraping
   - Inherits from `Orcid` class
   - Scrapes public ORCID profiles without authentication
   - Converts XML responses to JSON and reformats to match API structure
   - Only works with public profiles
   - Overrides `__read_section()` to use web scraping instead of API calls

4. **`OrcidSearch` (orcid_search.py)** - Wrapper for ORCID Search API
   - `search(query, start, rows, search_mode, columns)` - Searches ORCID registry
   - Supports three search modes: "expanded-search", "search", "csv-search"
   - Handles query encoding and pagination
   - Requires access token for authentication

### API Modes

The library supports two ORCID API modes:
- **Public API** (`state="public"`): Read-only access to public profiles, uses `pub.orcid.org`
- **Member API** (`state="member"`): Read/write access for ORCID members, uses `api.orcid.org`

Both modes support sandbox environments for testing (`sandbox=True` parameter).

### Data Processing Pipeline

1. **Token validation**: All classes except `OrcidScrapper` validate tokens on initialization
2. **API requests**: Made via `__read_section(section)` private method
3. **Data extraction**: Helper methods like `__get_value_from_keys()` navigate nested JSON safely
4. **Formatting**: Methods like `get_formatted_date()` convert API data to user-friendly formats
5. **Unicode handling**: `__deunicode_string()` removes non-ASCII characters for compatibility

### Testing Approach

Tests use mocked HTTP requests (unittest.mock) to avoid live API calls. The main `Orcid` class includes special `__test_*` methods that pull credentials from environment variables (`ORCID_ACCESS_TOKEN`) for CI/CD integration with GitHub Actions.

## Important Patterns

- **Private methods**: Methods prefixed with `__` (double underscore) are internal-only
- **Error handling**: Token validation occurs in `__init__()` for early failure detection
- **Return tuples**: Section methods typically return `(simplified_data, raw_data)` to provide both convenience and full access
- **Safe navigation**: `__get_value_from_keys()` prevents KeyError on missing nested keys
- **Inheritance**: `OrcidScrapper` extends `Orcid` to reuse data processing logic while changing the data source

## Dependencies

Core dependencies:
- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- `urllib3` - URL handling and encoding
- `xmltojson` - XML to JSON conversion (for scraping)

Development dependencies:
- `pytest` - Testing framework
- `flake8` - Linting (used in CI/CD)

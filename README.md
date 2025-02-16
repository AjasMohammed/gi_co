# Gi Co

## Project Overview
The `gi_co` project implements a Django application with the following functionalities:

- **API Endpoint**: `/accounts/user-data`
  - Supports `GET` and `POST` requests.
  - `POST` accepts CSV files, parses them, and stores valid records.
  - `GET` retrieves all user data in JSON format.

### API Response Format
```json
{
    "data": [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": "200",
            "status": {
                "errors": {
                    "age": ["Age should be between 0 and 120!"]
                }
            }
        }
    ],
    "rejected": 3,
    "success": 10,
    "total": 13
}
```

### Middleware
- Middleware tracks requests based on IP address.
- Blocks requests after 100 requests in a rolling 5-minute window.
- Returns HTTP 429 status code for blocked requests.

## Installation

### Prerequisites
- Python 3.x
- Redis server running locally on the default port.

### Installing UV Package Manager
```bash
pip install uv
```

### Installing Packages
The dependencies are managed with `uv` and stored in a `pyproject.toml` file. To install the dependencies, run:
```bash
uv pip install -r pyproject.toml
```

Alternatively, with `pip`:
```bash
pip install -r requirements.txt
```

## Running the Application

### Starting the Development Server
```bash
python manage.py runserver
```

### Running Tests
Test data is provided in the file `data.csv` in the root folder.
Navigate to the Project root folder. and run the command:
```bash
pytest
```

To generate an HTML test report:
```bash
pytest --html=test_report.html --self-contained-html
```

## Configuration
- Ensure Redis server is running locally on the port `6379`.
- Update Redis settings in `settings.py` if using a different configuration.

## Testing
- API tested using Postman.

## Notes
- The project uses `uv` for dependency management instead of `pip`.


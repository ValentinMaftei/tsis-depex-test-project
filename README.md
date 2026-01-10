# FastAPI Task Management Application

A simple FastAPI application for task management with comprehensive unit tests. This project is designed to demonstrate a basic FastAPI setup and serve as a test project for integrating Depex (a CI tool for dependency vulnerability detection) into your pre-deploy CI/CD pipeline.

## Features

- **Task Management API**: Create, read, update, and delete tasks
- **Health Check Endpoint**: Simple health status verification
- **FastAPI Documentation**: Interactive API documentation at `/docs`
- **Comprehensive Tests**: Full test coverage with pytest
- **Type Hints**: Full type annotations for better code quality
- **Validation**: Input validation using Pydantic models

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # Main FastAPI application with endpoints
│   └── models.py         # Pydantic models for request/response schemas
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Unit tests for all endpoints
├── requirements.txt      # Project dependencies
├── pyproject.toml        # Project configuration and tool settings
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Tasks
- `GET /tasks` - Get all tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Installation

### Prerequisites
- Python 3.9 or higher
- pip or conda

### Setup

1. Clone or navigate to the project directory:
```bash
cd tsis-depex-test-project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install with development dependencies:
```bash
pip install -e ".[dev]"
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app --cov-report=html
```

Run specific test class or function:
```bash
pytest tests/test_main.py::TestCreateTask::test_create_task_success
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
# or use your browser to open htmlcov/index.html
```

## Example API Usage

### Create a task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

### Get all tasks
```bash
curl "http://localhost:8000/tasks"
```

### Get health status
```bash
curl "http://localhost:8000/health"
```

### Update a task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "completed": true}'
```

### Delete a task
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Testing with Depex

This project is configured to work with Depex for dependency vulnerability detection. To integrate Depex into your CI/CD pipeline:

1. Ensure your `requirements.txt` or `pyproject.toml` is properly formatted
2. Configure Depex in your CI/CD pipeline to run in the pre-deploy phase
3. Depex will scan all dependencies and their versions for known vulnerabilities

### Sample Depex Configuration for CI/CD

You can add Depex to your CI/CD pipeline by creating a configuration file or adding it to your existing pipeline steps. This will help catch dependency vulnerabilities before deployment.

## Development

### Code Quality Tools

The project includes configuration for:
- **Black**: Code formatting (configured in `pyproject.toml`)
- **Flake8**: Linting
- **MyPy**: Static type checking
- **Pytest**: Testing and coverage

Run formatters and linters:
```bash
black app tests
flake8 app tests
mypy app
```

## License

MIT License - See LICENSE file for details

## Contributing

Feel free to submit issues and enhancement requests!

# API Tests

This directory contains comprehensive tests for the chatbot API.

## Test Structure

- **`conftest.py`** - Pytest configuration and fixtures
- **`test_api_basic.py`** - Basic API functionality tests
- **`test_multi_user.py`** - Multi-user API tests with parametrization
- **`run_tests.py`** - Test runner script

## Running Tests

### Prerequisites
1. Make sure the FastAPI server is running:
   ```bash
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Ensure the database is set up with test data:
   ```bash
   poetry run python create_tables.py
   poetry run python seed.py
   ```

### Running All Tests
```bash
# Using pytest directly
poetry run pytest

# Using the test runner
python tests/run_tests.py
```

### Running Specific Tests
```bash
# Run only basic tests
poetry run pytest tests/test_api_basic.py

# Run only multi-user tests
poetry run pytest tests/test_multi_user.py

# Run tests by class name
poetry run pytest -k "TestBasicAPI"
poetry run pytest -k "TestMultiUserAPI"
```

### Running with Coverage
```bash
poetry run pytest --cov=. --cov-report=html
```

## Test Categories

### Basic API Tests
- Tests fundamental API functionality
- User authentication and authorization
- Message sending and receiving
- Error handling for invalid requests

### Multi-User Tests
- Tests multi-user functionality with parametrization
- User isolation and thread management
- Message persistence across users
- API key validation and rejection

## Test Data

Tests use the following API keys:
- **Alice**: `alice_key_123`
- **Bob**: `bob_key_456`
- **Charlie**: `charlie_key_789`

## Fixtures

The `conftest.py` file provides several useful fixtures:
- `base_url` - API base URL
- `api_keys` - Dictionary of test API keys
- `alice_headers`, `bob_headers`, `charlie_headers` - Pre-configured headers for each user
- `invalid_headers` - Headers with invalid API key
- `json_headers` - Headers for JSON requests

## Example Test

```python
def test_user_authentication(self, base_url: str, alice_headers: Dict[str, str]):
    """Test Alice's authentication"""
    response = requests.get(f"{base_url}/users/me", headers=alice_headers)
    assert response.status_code == 200, "Alice should be able to authenticate"
    
    user_info = response.json()
    assert user_info["name"] == "Alice", "Should return Alice's info"
```

## Test Coverage

The test suite provides comprehensive coverage of:
- User authentication and authorization
- Multi-user functionality
- Message sending and receiving
- Error handling and validation
- API endpoint functionality
- Database persistence

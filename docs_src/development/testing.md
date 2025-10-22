# Testing Guide

This guide covers how to run and write tests for the VTS API project.

## Running Tests

### Run All Tests

```bash
# Using pytest directly
pytest

# Using the test runner script
python run_tests.py
```

### Run Specific Tests

```bash
# Run tests in a specific file
pytest tests/user/test_user_service.py

# Run a specific test function
pytest tests/user/test_user_service.py::test_create_user

# Run tests matching a pattern
pytest -k "test_create"
```

### Test Coverage

```bash
# Run tests with coverage report
pytest --cov=mod --cov=config --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

## Writing Tests

### Test Structure

Tests are organized by module:

```
tests/
├── conftest.py          # Shared fixtures
├── user/
│   ├── test_user_service.py
│   ├── test_user_repository.py
│   └── test_user_controller.py
```

### Example Test

```python
import pytest
from mod.user_mgmt.user_service import UserService
from mod.user_mgmt.UserDTO import UserCreateDTO

def test_create_user(db_session):
    """Test creating a new user."""
    service = UserService()
    
    user_data = UserCreateDTO(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    
    result = service.create_user(db_session, user_data)
    
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.id is not None
```

### Using Fixtures

Fixtures are defined in `conftest.py` and provide reusable test components:

```python
# In your test file
def test_get_user_by_id(db_session, sample_user):
    """Test retrieving a user by ID."""
    service = UserService()
    
    result = service.get_user_by_id(db_session, sample_user.id)
    
    assert result.id == sample_user.id
    assert result.username == sample_user.username
```

## Test Configuration

Test settings are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short"
```

## Best Practices

### 1. Isolation
Each test should be independent and not rely on other tests.

### 2. Clean Up
Use fixtures with teardown to clean up test data:

```python
@pytest.fixture
def test_user(db_session):
    user = create_test_user(db_session)
    yield user
    # Cleanup
    db_session.delete(user)
    db_session.commit()
```

### 3. Descriptive Names
Use clear, descriptive test names:

```python
# Good
def test_create_user_with_duplicate_email_raises_exception():
    pass

# Bad
def test_user_1():
    pass
```

### 4. Arrange-Act-Assert
Structure tests clearly:

```python
def test_update_user():
    # Arrange
    user = create_user()
    update_data = UserUpdateDTO(first_name="Updated")
    
    # Act
    result = service.update_user(db, user.id, update_data)
    
    # Assert
    assert result.first_name == "Updated"
```

### 5. Test Edge Cases
Don't just test happy paths:

```python
def test_get_nonexistent_user_raises_404():
    with pytest.raises(HTTPException) as exc:
        service.get_user_by_id(db, user_id=99999)
    assert exc.value.status_code == 404
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Before deployments

Ensure all tests pass before submitting code changes.

## Debugging Tests

### Run with verbose output
```bash
pytest -v -s
```

### Run with debugger
```bash
pytest --pdb
```

### Show print statements
```bash
pytest -v -s
```

## Performance Tests

For performance testing, use pytest-benchmark:

```python
def test_bulk_user_creation_performance(benchmark):
    result = benchmark(create_bulk_users, count=1000)
    assert result > 0
```

## Integration Tests

Integration tests test multiple components together:

```python
@pytest.mark.integration
def test_user_creation_workflow(client):
    """Test complete user creation via API."""
    response = client.post(
        "/api/users",
        json={
            "username": "newuser",
            "email": "new@example.com"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
```

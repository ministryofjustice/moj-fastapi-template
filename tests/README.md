# How to run tests
Tests are run using Pytest and can be run using:
```bash
pytest
```

# How to write API tests
Tests which send requests to an endpoint should use the client fixture defined in `tests/conftest.py`.

This client is a `fastapi.TestClient` object which allows you to mock sending requests without an HTTP or socket connection.

### Using the TestClient
To implement this client add it as an argument to your test function as shown:
```python
from fastapi.testclient import TestClient

def test_endpoint(client: TestClient):
    pass
```

This TestClient implements sending requests similarly to the requests module.

```python
from fastapi.testclient import TestClient

def test_endpoint(client: TestClient):
    response = client.get("/endpoint")
    assert response.status_code == 200
```

```python
from fastapi.testclient import TestClient

def test_endpoint(client: TestClient):
    response = client.post("/endpoint", json={"key": "value"})
    assert response.status_code == 201
```
View the full documentation for the TestClient [here](https://fastapi.tiangolo.com/reference/testclient/).

## Mocking the database
When we run unit tests we do not want to be writing to be writing to a permanent database.

We instead mock the database using an in-memory sqlite database, which is destroyed after each test.

This is handled for us when we use the client pytest fixture, discussed above. This TestClient overwrites the database
used by each endpoint.

If you want direct access to this in-memory database for your tests you simply need to include the session fixture
defined in `tests/conftest.py`.

```python
from sqlmodel import Session, select
from app.models import Case
from datetime import datetime as dt


def test_database(session: Session):
    # Create a new case object
    case = Case(id=1, name='test', category='Housing', time=dt.now())
    session.add(case)  # Write it to the database

    db_case = session.get(Case, 1)  # Read case with ID: 1 from the database
    assert db_case == case  # Assert they are equal
```
This session is a `sqlmodel.Session` object, it inherits from the SQLAlchemy session class.
View the SQLModel documentation [here](https://sqlmodel.tiangolo.com/).
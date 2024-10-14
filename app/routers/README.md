# Creating new endpoints
To create new endpoints you need to define the URL route it belongs to and which request method it accepts.

## APIRouter
Each route needs to belong to an APIRouter. APIRouters are analogous to Flask Blueprints in that they group endpoints
together and can be assigned shared a prefix, tags and other attributes.

See [here](https://fastapi.tiangolo.com/reference/apirouter/) for the documentation on the APIRouter class.

```python
from fastapi import APIRouter
from sqlmodel import SQLModel
from app.models.category_model import Categories

router = APIRouter(prefix="/case",
                   tags=["cases"])


@router.get("/{case_id}")
async def read_case(case_id: int):
    # We will discuss how to read from the database below.
    case = {"id": 1,
            "name": "test",
            "category": "Housing"}
    return case


class Case(SQLModel):
    name: str  # Pydantic ensures the name is always a string
    category: Categories | None = None  # This means that the category must be of the type Categories or None


@router.post("/")
async def create_case(case: Case):
    return case
```
These create_case route only accepts post requests and requires the request body to be of the form defined by
the Case model. 

This means the body needs to contain a name which can be encoded as a string and a category which 
matches one of the categories of law defined in the [/app/models/categories.py](../models/category_model.py) enum class.

To learn more about models please read [/app/models/README.md](../models/README.md)

## Reading and writing to the database
Database connections are managed with SQLModel sessions, these are inherited from SQLAlchemy sessions.

If your endpoint depends on a database session you can pass this into your routing function using the 
FastAPI `Depends()` method.

```python
from fastapi import APIRouter, HTTPException, Depends
from app.models.case_model import CaseRequest, Case
from sqlmodel import Session, select
from app.db import get_session
from datetime import datetime

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{case_id}", tags=["cases"])
async def read_case(case_id: str, session: Session = Depends(get_session)):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.post("/", tags=["cases"], response_model=Case)
def create_case(request: CaseRequest, session: Session = Depends(get_session)):
    case = Case(category=request.category, time=datetime.now(), name=request.name, id=1)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case
```
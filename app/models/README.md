# What are models?
Models are classes which define both the API and database schema.

Each field has Python type annotations which defines what data is accepted by the API 
as well as the column type in the database.

Every object created from these classes is validated by Pydantic, which ensures that the types of every object matches
the type defined in the model, always.

View the SQLModel documentation [here](https://sqlmodel.tiangolo.com/).

## What data types can I use in models?
All datatypes supported by Pydantic can be used, and you can define your own if needed.

View the Pydantic documentation [here](https://docs.pydantic.dev/latest/concepts/types/#constrained-types).

To allow for a set of values you can define an enum and use this in your model.
```python
from enum import Enum
from sqlmodel import SQLModel, Field


class Month(str, Enum):
    # jan will be stored in the database and "January" will be an acceptable input.
    jan = "January"
    fed = "February"
    mar = "March"


class Birthday(SQLModel):
    day: int = Field(gt=0, le=31)  # A number greater than 0 but less than or equal to 31.
    month: Month # Valid inputs would be "January", "February", "March"
```

## How do I create a database table?
By default, models will not be created as a table in the database. 

This is because we use models to define more than the database, they also define request and response 
models from the API.

To create a table with the schema defined by your model set the `table` argument on your class to True.
```python
from sqlmodel import SQLModel


class MyModel(SQLModel, table=True):
    name: str
    age: int
```

To reflect this new model in the database you will need to generate and run an Alembic migration.

Please see [/migrations/README.md](../db/migrations/README.md) for instructions on how to do this.

## How do I use these models to define endpoint schemas?
By implementing them as part of your routers' method arguments they are automatically used to validate the user's input.
```python
from app.models.cases import Case, CaseRequest
from app.routers.case_information import router


@router.post("/", tags=["cases"], response_model=Case)
def create_case(request: CaseRequest):
    pass
```

To see more about defining endpoints view the readme: [here](../routers/README.md).

### Model documentation
Your models will automatically be added to the Swagger documentation when you use them as part of an API endpoint.

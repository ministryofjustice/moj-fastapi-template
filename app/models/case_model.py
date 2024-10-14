from sqlmodel import Field, SQLModel
from app.models.base_model import TableModelMixin
from app.models.category_model import Category
from datetime import timedelta, datetime, UTC
from pydantic import computed_field


class CaseRequest(SQLModel):
    """Request model used to create a new case"""

    category: Category | None = Field()  # This field is optional


class Case(CaseRequest, TableModelMixin, table=True):
    """Model describing the Cases database schema and the response model for the read endpoint.
    The ID, created_at, and updated_at fields are provided by the TableModelMixin

    The properties aren't stored in the database, instead they are calculated each time the case is read
    and returned from the read route, or accessed from the object like any other attribute.
    """

    exceptional_funding: bool = Field(default=False)

    @computed_field
    @property
    def case_age(self) -> timedelta:
        return datetime.now(UTC) - self.created_at.replace(tzinfo=UTC)

    @computed_field
    @property
    def is_eligible(self) -> bool:
        return False  # This would call the eligibility API.

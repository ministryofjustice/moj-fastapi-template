from typing import Sequence

from fastapi import APIRouter, HTTPException, Depends

from app.models.cases import CaseRequest, Case
from app.models.users import User
from app.models.categories import Category
from sqlmodel import Session, select
from app.db import get_session
from app.auth.security import get_current_active_user
from uuid import UUID


router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{case_id}")
async def read_case(case_id: UUID, session: Session = Depends(get_session)) -> Case:
    """Get information about a given case ID."""
    case: Case | None = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.get("/")
async def read_all_cases(session: Session = Depends(get_session)) -> Sequence[Case]:
    """Read all the cases currently in the database."""
    cases = session.exec(select(Case)).all()
    return cases


@router.post("/", response_model=Case)
def create_case(request: CaseRequest, session: Session = Depends(get_session)) -> Case:
    """Creates a new case with a given category of law."""
    case = Case(**request.dict())
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


@router.put("/{case_id}", response_model=Case)
async def update_case(
    case_id: UUID, case_update: Case, session: Session = Depends(get_session)
):
    """Updates a case overwriting each field of an existing case with those present in the request body.
    Fields not included in the request body will be left unaltered.
    """
    case: Case | None = session.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    case_data = case_update.dict(exclude_unset=True)
    for key, value in case_data.items():
        setattr(case, key, value)

    session.add(case)
    session.commit()
    session.refresh(case)
    return case


@router.patch("/{case_id}", response_model=Case)
async def change_category(
    case_id: UUID, category: Category, session: Session = Depends(get_session)
):
    """Update a case category without changing any other attributes of the case."""
    case = session.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    case.category = category
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


@router.delete("/{case_id}", response_model=Case)
async def delete_case(
    case_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """The delete route cannot be used unless the user is authenticated due to the dependence on get_current_active_user"""
    case: Case | None = session.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    session.delete(case)
    session.commit()
    return case

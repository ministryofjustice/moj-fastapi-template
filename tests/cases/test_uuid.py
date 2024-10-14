import pytest
from app.models import Case
import uuid
from sqlmodel import Session
from pydantic import ValidationError


def test_id_is_uuid():
    case = Case()
    assert isinstance(case.id, uuid.UUID)


def test_uuid_collision(session: Session):
    """Tests attempting to cause a collision by manually creating two Cases with the same ID.
    The IDs should be re-generated  as they are being committed to the database rather than causing an IntegrityError.
    """
    case_id = uuid.UUID("1b08fd0e-724f-4d6b-af74-2b7ce3432dbc")
    case_1 = Case(id=case_id)
    case_2 = Case(id=case_id)
    session.add(case_1)
    session.add(case_2)
    assert case_1.id == case_id
    assert case_2.id == case_id
    session.commit()
    # As there was going to be a collision both UUIDs will be re-generated.
    assert case_1.id != case_id
    assert case_2.id != case_id


# This test will raise a warning around conflicting IDs, this is what we are testing for so can safely ignore it.
@pytest.mark.filterwarnings("ignore: New instance")
def test_existing_uuid_collision(session: Session):
    """Tests attempting to cause a collision by manually creating a case using the ID of another.
    The IDs should be re-generated as they are being committed to the database rather than causing an IntegrityError.
    """
    original_case = Case()
    session.add(original_case)
    original_id = original_case.id
    session.commit()
    new_case = Case(id=original_id)
    session.add(new_case)
    session.commit()
    assert new_case.id != original_case.id  # Ensure the new case gets a new ID
    assert (
        original_case.id == original_id
    )  # Ensure the original case keeps its original ID.


def test_invalid_uuid_int(session: Session):
    with pytest.raises(ValidationError):
        Case(id=1)


def test_invalid_uuid_str(session: Session):
    with pytest.raises(ValidationError):
        Case(id="string")

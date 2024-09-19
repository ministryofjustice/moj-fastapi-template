import logging
from sqlmodel import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import uuid

logger = logging.getLogger(__name__)


class CustomSession(Session):
    def commit(self, max_retries: int = 3) -> None:
        """Override the standard sqlmodel Session commit method, so we check for UUID4 Collisions as we are writing to
        the database writing to the database.
        Args:
            max_retries (int): Number of times to re-try generating UUIDs
        Raises:
            HTTPException: HTTP 500 is raised if unique UUIDs could not be generated.
        """
        retries = 0
        new_objects = self.new
        while retries < max_retries:
            try:
                return super().commit()  # Call the original commit method
            except IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    logger.error(e)
                    self.rollback()  # Rollback the database to the previous state so partial data does not persist
                    retries += 1
                    for instance in new_objects:
                        if hasattr(instance, "id") and isinstance(
                            instance.id, uuid.UUID
                        ):
                            logger.warning(
                                "UUID4 Collision Detected, generating a new UUID."
                            )
                            instance.id = uuid.uuid4()  # Regenerate UUID
                else:
                    raise e
        raise HTTPException(
            status_code=500,
            detail="Could not generate a unique UUID after multiple attempts.",
        )

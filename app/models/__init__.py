# All models defining DB Table schemas should be imported into this module this allows them to be
# found by Alembic when auto-generating migrations.
from .cases import Case  # noqa: F401
from .users import User  # noqa: F401

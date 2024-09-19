from sqlmodel import Field, SQLModel


class Token(SQLModel):
    """JSON Web Token (JWT) provided to the user after authentication."""

    access_token: str
    token_type: str


class TokenData(SQLModel):
    """TokenData links the JWT token to the username"""

    username: str | None = None


class User(SQLModel, table=True):
    """
    Users are required to be authenticated to use some functionality of the API.
    Disabled users are unable to authenticate to receive a token.
    """

    __tablename__ = "users"

    username: str = Field(primary_key=True)
    hashed_password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = Field(default=False)

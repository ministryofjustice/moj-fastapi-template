import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db import get_session
from app.models.user_model import User
from app.auth.security import get_password_hash
import logging


def add_users(users_list_dict: list[dict]):
    """
    This function creates new users in the spun up local database

    Args:
        users_list_dict: Should contain a list with a dictionary inside
        usernames and plain text passwords for users

    Logs:
        Logger warning: If username already exists will raise a
        warning and ignore adding this user. It was also raise
        a warning if there is a missing username/password.
    """
    with next(get_session()) as session:
        for user_info in users_list_dict:
            username = user_info.get("username")
            password = user_info.get("password")
            disabled = user_info.get("disabled")

            if not username or not password:
                logging.warning(
                    f"Skipping user with missing username or password: {user_info}"
                )
                continue

            # Check if the username already exists
            existing_user = session.get(User, username)
            if existing_user:
                logging.warning(f"User with username '{username}' already exists.")
                continue

            password = get_password_hash(password)
            new_user = User(
                username=username, hashed_password=password, disabled=disabled
            )
            session.add(new_user)

        session.commit()


users_to_add = [
    {"username": "test_user", "password": "test_password", "disabled": False},
]

add_users(users_to_add)

from fastapi.testclient import TestClient
from app.auth.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from freezegun import freeze_time
import pytest
from jwt import ExpiredSignatureError
from datetime import timedelta, datetime
from app.models.users import User
from uuid import uuid4


def test_auth_fail_case(client: TestClient):
    response = client.delete(f"/cases/{uuid4()}")
    json = response.json()
    assert json["detail"] == "Not authenticated"
    assert response.status_code == 401


def test_create_case_disabled_user(client: TestClient, auth_token_disabled_user):
    response = client.delete(
        f"/cases/{uuid4()}",
        headers={"Authorization": f"Bearer {auth_token_disabled_user}"},
    )
    json = response.json()
    assert json["detail"] == "User Disabled"
    assert response.status_code == 401


def test_username_token_fail(client: TestClient):
    response = client.post(
        "/token",
        data={"username": "fake_user", "password": "incorrect"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    json = response.json()
    assert json["detail"] == "Incorrect username or password"
    assert response.status_code == 401


def test_raw_token_fail(client: TestClient):
    response = client.post(
        "/token",
        data={"username": "cla_admin", "password": "cla_admin"},
        headers={"Content-Type": "raw"},
    )
    assert response.status_code == 422


def test_credential_exception(client: TestClient, auth_token):
    response = client.delete(
        "/cases/{uuid4()}", headers={"Authorization": f"Bearer {auth_token} + 1"}
    )
    json = response.json()
    assert json["detail"] == "Could not validate credentials"
    assert response.status_code == 401


def test_credential_exception_no_user(session, client: TestClient, auth_token):
    username = "test_user"
    user = session.get(User, username)
    session.delete(user)
    session.commit()
    response = client.delete(
        f"/cases/{uuid4()}", headers={"Authorization": f"Bearer {auth_token}"}
    )
    json = response.json()
    assert json["detail"] == "Could not validate credentials"
    assert response.status_code == 401


def test_authenticate_user(session):
    auth_user = authenticate_user(
        session=session, username="cla_admin", password="incorrect"
    )
    assert not auth_user


def test_password_hashing():
    hashed_password = "password"
    assert verify_password("password", get_password_hash(hashed_password))


def test_create_token():
    jwt = create_access_token(
        data={"sub": "cla_admin"}, expires_delta=timedelta(minutes=30)
    )
    assert len(jwt) == 129


def test_token_with_no_expire():
    with freeze_time("2024-08-23 10:00:00"):
        token = create_access_token(data={"sub": "cla_admin"})
        new_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 10)
    assert token is not None

    with freeze_time(new_time):
        assert pytest.raises(ExpiredSignatureError)


def test_token_defined_expiry():
    with freeze_time("2024-08-23 10:00:00"):
        token = create_access_token(
            data={"sub": "cla_admin"}, expires_delta=timedelta(minutes=1)
        )
    assert token is not None

    with freeze_time("2024-08-23 10:05:00"):
        assert pytest.raises(ExpiredSignatureError)

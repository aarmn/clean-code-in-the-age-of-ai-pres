import pytest
from fastapi.testclient import TestClient

from booking.api import create_app
from booking.domain import quote_cents


def test_quote_uses_integer_cents() -> None:
    assert quote_cents(2, 3500) == 7000


def test_quote_rejects_zero_seats() -> None:
    with pytest.raises(ValueError, match="at least one seat"):
        quote_cents(0, 3500)


def test_create_a_booking() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/bookings", json={"booking_id": "A42", "seats": 2})
        assert response.status_code == 201
        assert response.json() == {"booking_id": "A42", "seats": 2}


def test_duplicate_booking_returns_conflict() -> None:
    with TestClient(create_app()) as client:
        payload = {"booking_id": "A42", "seats": 2}
        assert client.post("/bookings", json=payload).status_code == 201
        assert client.post("/bookings", json=payload).status_code == 409


def test_zero_seats_returns_validation_error() -> None:
    with TestClient(create_app()) as client:
        payload = {"booking_id": "A42", "seats": 0}
        assert client.post("/bookings", json=payload).status_code == 422


def test_openapi_documents_create_and_conflict() -> None:
    with TestClient(create_app()) as client:
        schema = client.get("/openapi.json").json()
        responses = schema["paths"]["/bookings"]["post"]["responses"]
        assert {"201", "409", "422"} <= responses.keys()

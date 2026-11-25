import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from booking.domain import BookingAlreadyExists, BookingService, BookingStore
from booking.storage import MemoryBookingStore

logger = logging.getLogger(__name__)


class BookingRequest(BaseModel):
    booking_id: str = Field(min_length=1)
    seats: int = Field(ge=1)


class BookingResponse(BaseModel):
    booking_id: str
    seats: int


def create_app(store: BookingStore | None = None) -> FastAPI:
    app = FastAPI(title="Seat booking")
    service = BookingService(MemoryBookingStore() if store is None else store)

    @app.post(
        "/bookings",
        status_code=201,
        responses={409: {"description": "Booking ID already exists"}},
    )
    def create_booking(request: BookingRequest) -> BookingResponse:
        try:
            booking = service.create(request.booking_id, request.seats)
        except BookingAlreadyExists as exc:
            raise HTTPException(409, "Booking ID already exists") from exc

        logger.info("booking_created", extra={"seats": booking.seats})
        return BookingResponse(booking_id=booking.booking_id, seats=booking.seats)

    return app


app = create_app()

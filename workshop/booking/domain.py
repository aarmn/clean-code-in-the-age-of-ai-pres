from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Booking:
    booking_id: str
    seats: int


class BookingStore(Protocol):
    def get(self, booking_id: str) -> Booking | None: ...
    def save(self, booking: Booking) -> None: ...


class BookingAlreadyExists(Exception):
    pass


def quote_cents(seats: int, unit_price_cents: int) -> int:
    if seats < 1:
        raise ValueError("Book at least one seat")
    return seats * unit_price_cents


class BookingService:
    def __init__(self, store: BookingStore) -> None:
        self.store = store

    def create(self, booking_id: str, seats: int) -> Booking:
        if self.store.get(booking_id) is not None:
            raise BookingAlreadyExists(booking_id)

        booking = Booking(booking_id, seats)
        self.store.save(booking)
        return booking

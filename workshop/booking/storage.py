from booking.domain import Booking


class MemoryBookingStore:
    def __init__(self) -> None:
        self.bookings: dict[str, Booking] = {}

    def get(self, booking_id: str) -> Booking | None:
        return self.bookings.get(booking_id)

    def save(self, booking: Booking) -> None:
        self.bookings[booking.booking_id] = booking

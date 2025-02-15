from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.data_access_object import Booking_Data_Access_Object
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await Booking_Data_Access_Object.select_all_filter_by(user_id=user.id)

@router.post("")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await Booking_Data_Access_Object.add(
        user.id,
        room_id,
        date_from,
        date_to
    )
    booking_dict = parse_obj_as((SBooking, booking)).dict()
    if not booking:
        raise RoomCannotBeBooked
    send_booking_confirmation_email.delay(booking, user.email)
    return booking_dict



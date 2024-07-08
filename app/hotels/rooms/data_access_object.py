from datetime import date

from app.bookings.data_access_object import Booking_Data_Access_Object
from app.data_access_object.base import Base_Data_Access_Object
from app.hotels.models import Rooms
from app.hotels.rooms.schemas import SRooms


class RoomsDAO(Base_Data_Access_Object):
    model = Rooms

    @classmethod
    async def get_available_rooms_by_hotel_id(cls, hotel_id: int, date_from: date, date_to: date):
        result: list = []
        # get all rooms by hotel id
        rooms: list[SRooms] = [
            room for room in await cls.select_all_filter(Rooms.hotel_id == hotel_id)
        ]
        # get all available rooms
        for room in rooms:
            rooms_qty = room.quantity
            rooms_booked: int = len(
                await Booking_Data_Access_Object.get_booking_rooms_by_id(room.id, date_from, date_to)
            )
            rooms_left: int = int(rooms_qty) - int(rooms_booked)
            if rooms_left:
                room.rooms_left = rooms_left
                result.append(room)
        return result
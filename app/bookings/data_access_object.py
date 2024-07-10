from datetime import date

from pydantic import parse_obj_as
from sqlalchemy import select, func, and_, or_, insert
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking
from app.data_access_object.base import Base_Data_Access_Object
from app.database import async_session_maker
from app.hotels.models import Rooms
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import Users

class Booking_Data_Access_Object(Base_Data_Access_Object):
    model = Bookings

    @classmethod
    async def get_booking_for_user(cls, user: Users) -> list[SBooking]:
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.user_id,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(Bookings.user_id == user.id)
            )
            result = await session.execute(query)
            return result.all()

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            rooms_left = (
                select((Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"))
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left = await session.execute(rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                new_booking_dict = parse_obj_as(SBooking, new_booking)


                await session.commit()\
                send_booking_confirmation_email.delay()
                return new_booking_dict
            else:
                return None

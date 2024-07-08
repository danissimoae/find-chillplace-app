from fastapi import APIRouter

from app.hotels.data_access_object import Hotels_Data_Access_Object
from app.hotels.schemas import SHotels

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
async def get_hotels_by_location(location: str):
    """Get hotels by location"""
    hotels = await Hotels_Data_Access_Object.find_hotels_by_location(location)
    return hotels


@router.get("/all")
async def get_all_hotels():
    """Get all hotels."""
    hotels = await Hotels_Data_Access_Object.select_all()
    return hotels


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotels:
    """Get hotel by id."""
    hotel = await Hotels_Data_Access_Object.select_one_or_none_filter_by(id=hotel_id)
    return hotel
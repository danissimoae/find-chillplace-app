from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from app.hotels.router import get_all_hotels

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд часть"]
)

tempaltes = Jinja2Templates(directory="templates")

@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_all_hotels)
):
    return tempaltes.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )
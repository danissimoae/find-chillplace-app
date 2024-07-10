from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from app.hotels.router import get_all_hotels

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд часть"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_all_hotels)
):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request}
    )
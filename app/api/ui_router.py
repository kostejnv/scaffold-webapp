import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.settings import Settings

router = APIRouter(
    # prefix="/ui",
)

settings = Settings()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="static/templates")

@router.get("/test")
def testing_page(request: Request):
    """Render the testing page."""
    logger.info("Rendering the testing page")
    return templates.TemplateResponse("test.html", {"request": request})

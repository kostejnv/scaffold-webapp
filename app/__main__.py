import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.router import router
from app.api.ui_router import router as ui_router

app = FastAPI(
    title="ProjectName",
    description="ProjectName is a tool for XYZ.",
    version="0.1.0",
)

app.include_router(router)
app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

# logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
)

@app.get("/")
def index(request: Request):
    """Index page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health-check")
def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(status_code=status.HTTP_200_OK, content={"response": "running"})

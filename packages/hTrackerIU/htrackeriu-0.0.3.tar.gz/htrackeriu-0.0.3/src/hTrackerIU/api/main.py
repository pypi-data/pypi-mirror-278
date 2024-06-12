import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routes import router

environment = os.getenv("ENV", "prod")
react_app_port = os.getenv("REACT_APP_PORT", "3000")

app = FastAPI()

if environment != "prod":
    origins = [
        "http://localhost:" . react_app_port,
        "http://127.0.0.1:" . react_app_port,
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix="/api")

BASE_DIR = Path(__file__).resolve().parent.parent
static_files_path = BASE_DIR / "static" / "static"

if environment == "prod":
    app.mount(
        "/static",
        StaticFiles(
            directory=str(static_files_path)),
        name="static")

    static_index_path = BASE_DIR / "static" / "index.html"

    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def catch_all(request: Request, full_path: str):
        if ".." in full_path:
            return HTMLResponse("Access Denied", status_code=403)

        file_path = BASE_DIR / "static" / full_path

        if file_path.suffix in ['.png', '.json', '.ico', '.js']:
            if file_path.is_file():
                return FileResponse(file_path)
            else:
                return HTMLResponse("File not found", status_code=404)

        if not request.url.path.startswith("/api"):
            return static_index_path.read_text()

        return HTMLResponse("Not found", status_code=404)

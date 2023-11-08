import sys
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import router

# ----------------------- #

app = FastAPI()

app.mount(
    "/frontend",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "frontend"),
    name="frontend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:8125"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ....................... #

api_router = APIRouter()


@api_router.get("/health")
async def health_check():
    return {"status": "ok"}


api_router.include_router(router)
app.include_router(api_router)
# ....................... #

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8094, reload=True)

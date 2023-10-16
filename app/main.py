from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router
# ----------------------- #

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    uvicorn.run("main:app", host="0.0.0.0", port=8020, reload=True)
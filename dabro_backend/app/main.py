from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.router import router

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
#     return JSONResponse(
#         status_code=422,
#         content={
#             "error": "validation_error",
#             "detail": exc.errors()
#         },
#     )

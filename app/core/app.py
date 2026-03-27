import logfire
from fastapi import FastAPI

from app.core.settings import Settings

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="app",
    environment=settings.environment,
    console=False,
)

app = FastAPI()

logfire.instrument_fastapi(app, capture_headers=True, extra_spans=True)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

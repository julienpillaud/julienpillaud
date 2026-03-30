import datetime

from fastapi import status
from pydantic import BaseModel


class TempData(BaseModel):
    title: str
    message: str
    status_code: int
    status: str
    last_update: str


def generate_data(
    message: str = "OK",
    status_code: int = status.HTTP_200_OK,
) -> TempData:
    return TempData(
        title="CV",
        message=message,
        status_code=status_code,
        status="IN_PROGRESS" if status_code == status.HTTP_200_OK else "ERROR",
        last_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

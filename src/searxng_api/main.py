from typing import List, Literal, Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRoute

from .schemas import GeneralSearchResult, ImageSearchResult
from .services import search

app = FastAPI()


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "OK"


@app.get("/search/general", response_model=List[GeneralSearchResult])
async def search_general(
    q: str,
    language: Optional[str] = "ja",
    page: int = 1,
    time_range: Optional[Literal["day", "month", "year"]] = None,
    format: Optional[Literal["json", "csv", "rss"]] = "json",
) -> List[GeneralSearchResult]:
    return await search(
        q=q,
        engine_type="general",
        language=language,
        page=page,
        time_range=time_range,
        format=format,
    )


@app.get("/search/images", response_model=List[ImageSearchResult])
async def search_images(
    q: str,
    language: Optional[str] = "ja",
    page: int = 1,
    time_range: Optional[Literal["day", "month", "year"]] = None,
    format: Optional[Literal["json", "csv", "rss"]] = "json",
) -> List[ImageSearchResult]:
    return await search(
        q=q,
        engine_type="images",
        language=language,
        page=page,
        time_range=time_range,
        format=format,
    )


def simplify_client_method_names(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


simplify_client_method_names(app)

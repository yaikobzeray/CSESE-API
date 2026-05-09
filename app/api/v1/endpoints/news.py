from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import news as crud
from app.models.news import NewsCategory
from app.schemas.news import NewsCreate, NewsOut, NewsUpdate

router = APIRouter(tags=["News"])


@router.get("/", response_model=list[NewsOut])
def list_news(
    db: DbSession,
    category: Annotated[NewsCategory | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 20,
):
    return crud.get_all_news(db, published_only=True, category=category, skip=skip, limit=limit)


@router.get("/{news_id}", response_model=NewsOut)
def get_news(news_id: int, db: DbSession):
    item = crud.get_news(db, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    return item


@router.post("/", response_model=NewsOut, status_code=status.HTTP_201_CREATED)
def create_news(data: NewsCreate, db: DbSession, _: CurrentAdmin):
    return crud.create_news(db, data)


@router.patch("/{news_id}", response_model=NewsOut)
def update_news(news_id: int, data: NewsUpdate, db: DbSession, _: CurrentAdmin):
    item = crud.get_news(db, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    return crud.update_news(db, item, data)


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(news_id: int, db: DbSession, _: CurrentAdmin):
    item = crud.get_news(db, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    crud.delete_news(db, item)

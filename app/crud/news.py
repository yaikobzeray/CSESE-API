from sqlalchemy.orm import Session

from app.models.news import News, NewsCategory
from app.schemas.news import NewsCreate, NewsUpdate


def get_news(db: Session, news_id: int) -> News | None:
    return db.get(News, news_id)


def get_all_news(
    db: Session,
    *,
    published_only: bool = True,
    category: NewsCategory | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[News]:
    q = db.query(News)
    if published_only:
        q = q.filter(News.is_published == True)  # noqa: E712
    if category:
        q = q.filter(News.category == category)
    return q.order_by(News.publish_date.desc()).offset(skip).limit(limit).all()


def create_news(db: Session, data: NewsCreate) -> News:
    news = News(**data.model_dump())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def update_news(db: Session, news: News, data: NewsUpdate) -> News:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(news, field, value)
    db.commit()
    db.refresh(news)
    return news


def delete_news(db: Session, news: News) -> None:
    db.delete(news)
    db.commit()

from datetime import datetime
from typing import Optional

from pydantic import BaseSettings
from sqlmodel import Field, SQLModel, create_engine


class DotEnv(BaseSettings):
    IS_DEV: bool
    DB_URL: str

    class Config:
        env_file = ".env"


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linkedin_id: Optional[str] = Field(index=True)
    url: Optional[str]
    title: Optional[str]
    location: Optional[str]
    posting_date: Optional[datetime]
    company_name: Optional[str]
    company_url: Optional[str]
    is_visited: bool = False


env_settings = DotEnv()

engine = create_engine(env_settings.DB_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)

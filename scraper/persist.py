from datetime import datetime
from typing import Optional

from pydantic import BaseSettings
from sqlmodel import Field, SQLModel, create_engine


class DotEnv(BaseSettings):
    IS_DEV: bool
    USER: str
    PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_URL: str = None

    class Config:
        env_file = ".env"


class DevJobs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linkedin_id: Optional[str] = Field(index=True)
    url: Optional[str]
    title: Optional[str]
    location: Optional[str]
    posting_date: Optional[str]
    company_name: Optional[str]
    company_url: Optional[str]
    is_visited: bool = False


env_settings = DotEnv()

if env_settings.IS_DEV:
    engine = create_engine(url="sqlite:///job_dev.db")
else:
    engine = create_engine(
        url=f"postgresql://{env_settings.USER}:{env_settings.PASSWORD}@{env_settings.DB_HOST}/{env_settings.DB_NAME}"
    )


def create_tables():
    SQLModel.metadata.create_all(engine)

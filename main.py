# from scraper.persist import get_sheet
import sys

import functions_framework
from flask import Request
from loguru import logger
from sqlmodel import Session

from scraper.collect import JobCollector
from scraper.persist import DevJobs, create_tables, engine, env_settings

logger.remove()
if env_settings.IS_DEV:
    logger.add(sys.stderr, level="DEBUG")
else:
    logger.add(sys.stderr, level="INFO")


@functions_framework.http
def main(request: Request):
    params = request.json
    collector = JobCollector(**params)
    job_generator = collector.collect()
    create_tables()
    with Session(bind=engine) as db_session:
        for i, job in enumerate(job_generator):
            db_session.add(
                DevJobs(
                    linkedin_id=job[0],
                    url=job[1],
                    title=job[2],
                    location=job[3],
                    posting_date=job[4],
                    company_name=job[5],
                    company_url=job[6],
                )
            )
            logger.debug(job[0])
            if i % 50 == 0:
                db_session.commit()
        db_session.commit()

    return {"count": collector.count}

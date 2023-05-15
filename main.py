# from scraper.persist import get_sheet
import sys

import functions_framework
from flask import Request
from loguru import logger

from scraper.collect import JobCollector

logger.remove()
logger.add(sys.stderr, level="DEBUG")


@functions_framework.http
def main(request: Request):
    params = request.json
    collector = JobCollector(**params)
    job_generator = collector.collect()
    for job in job_generator:
        logger.debug(job)

    return {"count": collector.count}


# if __name__ == "__main__":
#     main()

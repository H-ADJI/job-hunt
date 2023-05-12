# from scraper.persist import get_sheet
import sys

import functions_framework
from flask import Request
from loguru import logger

from scraper.collect import JobCollector
from scraper.persist import Google_sheet
from scraper.strategy import Strategy

logger.remove()
logger.add(sys.stderr, level="INFO")


@functions_framework.http
def main(request: Request):
    strategy_data = request.json
    with Strategy(strategy_data=strategy_data) as strategy:
        with Google_sheet(strategy=strategy) as gs:
            collector = JobCollector()
            job_generator = collector.collect(strategy=strategy)
            for job in job_generator:
                gs.append(job)

    return collector.summary


# if __name__ == "__main__":
#     main()

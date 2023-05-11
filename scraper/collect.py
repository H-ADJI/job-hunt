from time import sleep, time

import parsel
import requests
from loguru import logger

from scraper.exceptions import EmptyJobPage
from scraper.parse import normalize_text
from scraper.strategy import Strategy
from scraper.utils import (
    HEADERS,
)


class JobCollector:
    JOB_SELECTOR = "body/li/div"
    JOB_TITLE = "./a/span/text()"
    JOB_URL = "./a/@href"
    JOB_LOCATION = "./div/div/span/text()"
    JOB_LISTING_DATE = "./div/div/time/@datetime"
    COMPANY_NAME = "./div/h4/a/text()"
    COMPANY_URL = "./div/h4/a/@href"
    JOB_PAGINATION_URL = "https://www.linkedin.com/jobs/api/seeMoreJobPostings/search"
    iteration_progress = 25

    def __init__(self) -> None:
        self.summary = {}

    def __paginate(self, session: requests.Session, params, progress):
        query_params = params | {"start": progress}
        response: requests.Response = session.get(self.JOB_PAGINATION_URL, params=query_params)
        return response.text, response.url, response.status_code

    def __extract_job(self, page_content):
        jobs_selected: parsel.SelectorList[parsel.Selector] = parsel.Selector(page_content).xpath(
            JobCollector.JOB_SELECTOR
        )
        if not jobs_selected:
            raise EmptyJobPage("No job to select in the current page")
        for selector in jobs_selected:
            yield (
                normalize_text(selector.xpath(JobCollector.JOB_TITLE).get()),
                normalize_text(selector.xpath(JobCollector.JOB_URL).get()),
                normalize_text(selector.xpath(JobCollector.JOB_LOCATION).get()),
                normalize_text(selector.xpath(JobCollector.JOB_LISTING_DATE).get()),
                normalize_text(selector.xpath(JobCollector.COMPANY_NAME).get()),
                normalize_text(selector.xpath(JobCollector.COMPANY_URL).get()),
            )

    def __log_metrics(self, starting_time: float, params: dict, progress: int, strategy: Strategy):
        summary = {
            params.get("keywords"): {
                "row_count": progress,
                "reached_limit": strategy.limit <= progress,
                "duration": time() - starting_time,
            }
        }
        self.summary[params.get("location")] = summary

    def show_summary(self):
        logger.info(self.summary)

    def collect(self, strategy: Strategy):
        combo_generator = strategy.generate_params_combo()

        with requests.session() as session:
            session.headers.update(HEADERS)
            for params in combo_generator:
                progress = 0
                start = time()
                while strategy.limit > progress:
                    content, url, status_code = self.__paginate(
                        session=session, params=params, progress=progress
                    )
                    logger.info(f"GET {url}")
                    logger.info(f"request for paginating to {progress} -  status : {status_code}")
                    sleep(strategy.request_period)

                    if status_code == 400:
                        logger.warning("Got an 400 error, porbably there are no mroe jobs listings")
                        break
                    elif status_code == 429:
                        logger.warning(
                            f"Got an 429 error, too many requests sleeping for {strategy.cooldown}"
                        )
                        sleep(strategy.cooldown)
                    else:
                        try:
                            jobs = self.__extract_job(page_content=content)
                            progress += self.iteration_progress
                        except EmptyJobPage:
                            logger.info(f"no jobs to grab from page after {progress} job")
                            break
                        for job in jobs:
                            logger.debug(job[0])
                            yield job
                self.__log_metrics(
                    starting_time=start, params=params, progress=progress, strategy=strategy
                )

    def content_filter(self):
        pass

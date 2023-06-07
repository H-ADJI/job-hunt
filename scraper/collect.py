import re
from time import sleep

import parsel
import requests
from loguru import logger

from scraper.exceptions import EmptyJobPage
from scraper.parse import normalize_text
from scraper.utils import (
    HEADERS,
)


class JobCollector:
    ID_REGEX_PATTERN = r"\d+(?=\?ref)"
    JOB_SELECTOR = "body/li/div"
    JOB_TITLE = "./a/span/text()"
    JOB_URL = "./a/@href"
    JOB_LOCATION = "./div/div/span/text()"
    JOB_LISTING_DATE = "./div/div/time/@datetime"
    COMPANY_NAME = "./div/h4/a/text()"
    COMPANY_URL = "./div/h4/a/@href"
    JOB_PAGINATION_URL = "https://www.linkedin.com/jobs/api/seeMoreJobPostings/search"
    iteration_progress = 25
    request_freq = 2
    cooldown = 20
    search_query = ["backend", "software engineer", "data engineer"]

    def __init__(self, location, timeframe=6) -> None:
        self.location = location
        # how old the jobs can be ( from hours -> seconds )
        self.timeframe = f"r{timeframe * 3600}"

    def __paginate(self, session: requests.Session, params, progress, query):
        query_params = params | {"keywords": query, "start": progress}
        response: requests.Response = session.get(self.JOB_PAGINATION_URL, params=query_params)
        return response.text, response.url, response.status_code

    def __extract_job(self, page_content):
        jobs_selected: parsel.SelectorList[parsel.Selector] = parsel.Selector(page_content).xpath(
            JobCollector.JOB_SELECTOR
        )
        if not jobs_selected:
            raise EmptyJobPage("No job to select in the current page")
        for selector in jobs_selected:
            url = normalize_text(selector.xpath(JobCollector.JOB_URL).get())
            match = re.search(self.ID_REGEX_PATTERN, url)
            id = None
            if match:
                id = match.group(0)
            yield (
                id,
                url,
                normalize_text(selector.xpath(JobCollector.JOB_TITLE).get()),
                normalize_text(selector.xpath(JobCollector.JOB_LOCATION).get()),
                normalize_text(selector.xpath(JobCollector.JOB_LISTING_DATE).get()),
                normalize_text(selector.xpath(JobCollector.COMPANY_NAME).get()),
                normalize_text(selector.xpath(JobCollector.COMPANY_URL).get()),
            )

    def collect(self):
        with requests.session() as session:
            session.headers.update(HEADERS)
            for query in self.search_query:
                progress = 0
                while True:
                    content, url, status_code = self.__paginate(
                        session=session,
                        params=dict(location=self.location, f_TPR=self.timeframe),
                        progress=progress,
                        query=query,
                    )
                    logger.debug(f"GET {url}")
                    logger.debug(f"request for paginating to {progress} -  status : {status_code}")
                    sleep(self.request_freq)

                    if status_code == 400:
                        logger.info("Got an 400 error, porbably there are no more jobs listings")
                        break
                    elif status_code == 429:
                        logger.info(
                            f"Got an 429 error, too many requests sleeping for {self.cooldown}"
                        )
                        sleep(self.cooldown)
                    else:
                        try:
                            jobs = self.__extract_job(page_content=content)
                            progress += self.iteration_progress
                            for job in jobs:
                                logger.debug(job[0])
                                yield job

                        except EmptyJobPage:
                            logger.info(f"no jobs to grab from page after {progress} job")
                            break
        self.count = progress

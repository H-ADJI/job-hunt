from time import sleep

import parsel
import requests

from scraper.parse import normalize_text
from scraper.utils import (
    COMPANY_NAME,
    COMPANY_URL,
    HEADERS,
    JOB_LISTING_DATE,
    JOB_LOCATION,
    JOB_PAGINATION_URL,
    JOB_SELECTOR,
    JOB_TITLE,
    JOB_URL,
    REQUEST_TIME_PERIOD,
)


def job_pagination(keywords: list[str], locations: list[str], cooldown: int = 15):
    try:
        s: requests.Session = requests.session()
        s.headers.update(HEADERS)
        for keyword in keywords:
            for location in locations:
                params: dict[str, str | int] = {"keywords": keyword, "location": location}
                job_count = 1
                progress = 0
                while job_count > 0:
                    params["start"] = progress
                    response: requests.Response = s.get(JOB_PAGINATION_URL, params=params)
                    print(f"GET {response.url}")
                    sleep(REQUEST_TIME_PERIOD)
                    print("-" * 20)
                    print(
                        f"request for paginating to {progress} -  status : {response.status_code}"
                    )
                    print("-" * 20)

                    if response.status_code == 400:
                        break
                    elif response.status_code == 429:
                        print(f"sleeping for {cooldown}")
                        sleep(cooldown)
                    else:
                        progress += 25
                        selectors: parsel.SelectorList[parsel.Selector] = parsel.Selector(
                            response.text
                        ).xpath(JOB_SELECTOR)
                        if not selectors:
                            print(f"no more elements, gathered {progress} elemnts")
                            break
                        for selector in selectors:
                            yield (
                                normalize_text(selector.xpath(JOB_TITLE).get()),
                                normalize_text(selector.xpath(JOB_URL).get()),
                                normalize_text(selector.xpath(JOB_LOCATION).get()),
                                normalize_text(selector.xpath(JOB_LISTING_DATE).get()),
                                normalize_text(selector.xpath(COMPANY_NAME).get()),
                                normalize_text(selector.xpath(COMPANY_URL).get()),
                            )
    finally:
        s.close()
        
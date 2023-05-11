JOB_DETAILS_URL = "https://www.linkedin.com/jobs/api/jobPosting/"
JOB_PAGINATION_URL = "https://www.linkedin.com/jobs/api/seeMoreJobPostings/search"

REQUEST_TIME_PERIOD = 2

JOB_SELECTOR = "body/li/div"
JOB_TITLE = "./a/span/text()"
JOB_URL = "./a/@href"
JOB_LOCATION = "./div/div/span/text()"
JOB_LISTING_DATE = "./div/div/time/@datetime"
COMPANY_NAME = "./div/h4/a/text()"
COMPANY_URL = "./div/h4/a/@href"
# --------------------------------------------------
JOB_DESCRIPTION = "//section[@class='show-more-less-html']//text()"
JOB_SENIORITY = "//li[@class = 'description__job-criteria-item'][1]/span/text()"
JOB_EMPLOYEMENT_TYPE = "//li[@class = 'description__job-criteria-item'][2]/span/text()"
JOB_FUNCTION = "//li[@class = 'description__job-criteria-item'][3]/span/text()"
JOB_INDUSTRY = "//li[@class = 'description__job-criteria-item'][4]/span/text()"

SPEACIAL_SEPARATOR = "|=|"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

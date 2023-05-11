from scraper.collect import job_pagination


def main():
    keywords = ["python", "javascript"]
    locations = ["morocco", "united kingdom", "france"]
    job_generator = job_pagination(keywords=keywords, locations=locations)
    for job in job_generator:
        print(job)


if __name__ == "__main__":
    main()

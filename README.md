# Job hunting

## linkedin reverse api

### Job listings

The job lists can be accessed trough the following **url** : https://www.linkedin.com/jobs/api/seeMoreJobPostings/search, while it doesn't require any authentication / authorization, this api is limited to 1request/sec.

The main query params that can be used to filter the job listing are :

- **location** : a string that indicate where the jobs are located
- **keywords** : a space separated string to filter relevant jobs

The data fields that can be accessed from this page are :

- job title
- job id
- job url
- job location
- job posting date
- company name
- company url

### Job details

The job details can be accessed either through the url collected from job listings page, or be appending the job id to the following **url** : https://ma.linkedin.com/jobs/view as a path param.

The data fields that can be accessed from this page are (in addition to the fields above) :

- job description
- job seniority
- job employement type
- job function
- job industry
- company id

### Company details

Requires account log in

# Job hunting

## Linkedin

Linkedin helps individuals find job opportunities by providing a platform to search for job listings, connect with professionals and companies, and showcase skills and experience through personal profiles, ultimately facilitating career advancement and networking.

While linkedin provide the access to job opportunities listing through an interface, I find it very **limited** in term of search parameters and filters.

Then the idea of collecting this data in order to have more control on what jobs to display according to a more flexible and accurate filtering mechanism and why not use it for personal purposes when looking for a job.

## Data Gathering

The method used to gather the data from the linkedin job page was to target the job's backend API directly since it will be easier to deal with (no JS rendering and browser overhead less headache parsing HTML).

Finding the url used to populate the linkedin job page was not that difficult. Here are some bread crumbs that anyone can apply to any website:

- Navigate to the page that contains the data you're interested in.
- Use isolated browsers contexts (aka private tabs) so that your cookies, extensions and cache doesn't interfere with the process.
- Disable Javascript permission from the page so that you know if the page comes pre-populated with data.
- In case no data is rendered when disabling javascript navigate to the network tab in the devtool and inspect the response of the network calls until you find the data you're looking for.
- Use CTRL+f extensively: grab some piece of data from the web page and go look for it in then elements + network tab within devtools.

This process is called API reverse engineering, my introduction to it was through Game cheating forums where gamers are figuring out how their favorite game's backend work, defeating cheat detection, and all of the other fine things in life. Shout out to [Reverse Engineering Games](https://www.reddit.com/r/REGames/) and [UnkownCheats](https://www.unknowncheats.me/forum/index.php).

Another, and probably, more efficient way of reverse engineering some applications API is to target their mobile version, and there is a great ecosystem of software made for inspecting mobile apps (mitmproxy, Proxyman, Charles, ...).

### Job listings

The job lists can be accessed through the following **url** : https://www.linkedin.com/jobs/api/seeMoreJobPostings/search, while it doesn't require any authentication / authorization, this API is limited to 1 request per 2s.

The main query params that can be used to filter the job listing are :

- **location** : a string that indicates where the jobs are located.
- **keywords** : a space separated string to filter relevant jobs.
- **f_TPR** : an int representing how old the jobs fetched are (in seconds).
- **start** : an int used to paginate the results.

The data fields that can be accessed from this page are :

- job title
- job id
- job url
- job location
- job posting date
- company name
- company url

### Job details

The job details can be accessed either through the url collected from the job listings page, or by appending the job id to the following **url** : https://ma.linkedin.com/jobs/view as a path param.

The data fields that can be accessed from this page are (in addition to the fields above) :

- job description
- job seniority
- job employment type
- job function
- job industry
- company id

### Company details

Requires account log in, unfortunately.

## Data Pipeline Architecture

### Architecture Diagram

![architecture image](/Linkedin_serverless_scraper.png "architecture")

### Explanation

While we could just host a scraping bot in a simple VM instance (AWS EC2 or GCP Compute Engine), and use the Unix CRON CLI to schedule the jobs, but serverless function is more favorable in this use case. Using function removes the strain to manage the infra and since our function will be running for no longer than 5 minutes for each execution, your billing account will thank you since you're not even above the free tier usage of whatever cloud provider you're using. Plus each time the functions are executed they are exposed with a different public IP address which removes the concern of getting IP banned for abusing the linkedin API with simultaneous function calls.

The GCP functions are responsible for running the data collection code. Each GCP Scheduler job triggers the function using an HTTP POST request with the body containing data about the **location** and the **timeframe** of the jobs, timeframe refers to how old the jobs that should be included.

For example a scheduling job that is running every 6 hours per day should only consider the jobs listed 6 hours ago, so the body of the request should look like this:

```json
{
    "location": "morocco",
    "timeframe": "6"
}
```

# Job hunting

## Linkedin

Linkedin helps individuals find job opportunities by providing a platform to search for job listings, connect with professionals and companies, and showcase skills and experience through personal profiles, ultimately facilitating career advancement and networking.

While linkedin provide the access to job opportunities listing through an interface, I find it very **limited** in term of search parameters and filters.

Then the idea of collecting this data in order to have more control on what jobs to display according to a more flexible and accurate filtering mechanisms and why not use it for personal purposes when looking for a job.

## Data Gathering

The method used to gather the data from linkedin job page was to target the job's backend API directly since it will be easier to deal with (no JS rendering and browser overhead less headache parsing HTML).

finding the url used to populate linkedin job page was not that difficult here are some breadcrumbs that anyone can apply to any website :

- Navigate to the page that contains the data you're interested in.
- Use isolated browsers contexts (aka private tabs) so that your cookies, extensions and cache doesn't interfer with the process.
- Disable Javascript permission from the page so that you know if the page commes pre-populated with data.
- In case no data is rendered when disabling javascript.
- navigate to the network tab in the devtool and inspect the responces of the network calls until you find the data you're looking for.
- Use CTRL+f extensively : grab some piece of data from the web page and go look for it in then elements + network tab withing devtools.

This process is called API reverse engineering, my introduction to it was through Game cheating forums where gamers are figuring out how their favorite game's backend work, defeating cheat detection, and all of the other fine things in life. shoutout to [Reverse Engineering Games](https://www.reddit.com/r/REGames/) and [UnkownCheats](https://www.unknowncheats.me/forum/index.php).

Another, and probably, more efficient way of reverse engineering some applications API is to target their mobile version, and there is a great ecosystem of software made for inspecting mobile apps (mitmproxy, Proxyman, Charles, ...).

### Job listings

The job lists can be accessed trough the following **url** : https://www.linkedin.com/jobs/api/seeMoreJobPostings/search, while it doesn't require any authentication / authorization, this api is limited to 1 request per 2s.

The main query params that can be used to filter the job listing are :

- **location** : a string that indicate where the jobs are located.
- **keywords** : a space separated string to filter relevant jobs.
- **f_TPR** : an int representing how old the job fetched are (in seconds).
- **start** : an int used to paginate over the results.

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

Requires account log in, unfortunatly.

## Data Pipeline Architecture

### Architecture Diagram



### Collection Strategy


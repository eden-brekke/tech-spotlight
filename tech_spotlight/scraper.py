import requests
import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup


"""
Scrape indeed.com for the job title software engineer

Example URL https://www.indeed.com/jobs?q=Software%20Engineer&l=remote&fromage=3&start=10&vjk=433b6a457d0b609e
Query = the job title to search
L = the location in put "remote" - "Seattle" etc.
fromage = the age of the posts, we will start with 3
start = we can increment this by 10 for each itteration to get new job posts each time.

We may also need to handle some job cards that are adds for indeed. (these can show up among the job posts)

within the job posts we want to scrape into id="jobDescriptionText"

find a way to itterate through the cards on indeed
for each card grab its id="jobDescriptionText" 
thats the document we are saving to later search for terms.
"""


def scraper(job_title, location, age):
    start = 0  # used to get new jobs within URL as a query
    scraped_jobs = 0  # Counter to display total num of scrapes performed
    scrapes = 30  # num of scrapes to do, (increments of 15 due to indeed page structure)

    while scraped_jobs < scrapes:
        # Structuring the URL can be broken into a new function
        # Input is query args, Output is formatted soup
        get_vars = {'q': job_title, 'l': location, 'fromage': age, 'start': start}
        url = 'https://www.indeed.com/jobs?' + urllib.parse.urlencode(get_vars)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        jobsearch_results = soup.find(class_='jobsearch-ResultsList')
        # end of soup kitchen funcitonality

        for list_elem in jobsearch_results:
            a_tag = list_elem.find('a')  # grabs all links by A tag.
            if a_tag:  # filters Nonetypes so we pass over those.

                scraped_jobs += 1  # scrape counter
                job_id = a_tag.get('data-jk')  # gets each job ID for a given A tag
                print(job_id + " Num scraped: " + scraped_jobs)  # prints ID and Num scraped.

                job_url = 'https://www.indeed.com/viewjob?jk=' + str(job_id)  # formats our URL

                # Function to take in URL and make soup
                page = requests.get(job_url)  # gets the page content
                post_soup = BeautifulSoup(page.content, 'html.parser')  # makes some soup

                description = post_soup.find(class_='jobsearch-jobDescriptionText')
                description = description.text
                with open('jobs_raw.txt', 'a+') as f:
                    f.write(description)
        start += 10
    print(scraped_jobs)

    return


def soup_kitchen(job_title, location, age, start):
    """
        # Structuring the URL can be broken into a new function
        # Input is query args, Output is formatted soup
        get_vars = {'q': job_title, 'l': location, 'fromage': age, 'start': start}
        url = 'https://www.indeed.com/jobs?' + urllib.parse.urlencode(get_vars)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        jobsearch_results = soup.find(class_='jobsearch-ResultsList')
        # end of soup kitchen funcitonality
    """
    get_vars = {'q': job_title, 'l': location, 'fromage': age, 'start': start}
    url = 'https://www.indeed.com/jobs?' + urllib.parse.urlencode(get_vars)
    soup = job_soup(url)
    results = soup.find(class_='jobsearch-ResultsList')
    return results


def job_soup(job_url):
    # Function to take in URL and make soup
    page = requests.get(job_url)  # gets the page content
    post_soup = BeautifulSoup(page.content, 'html.parser')  # makes some soup
    return post_soup


scraper('software engineer', 'remote', '3')

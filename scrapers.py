from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from company import serialize as serializeCompany
from review import serialize as serializeReviews
from math import floor
from utils import readFromFile


def scrape_companies(driver, wait, companies):
    successful = []
    failed = []
    print(f'Starting scraping companies! Total URLs {len(companies)}')
    for company in companies:
        try:
            driver.get(company.get('url'))
            wait.until(EC.presence_of_element_located((By.ID, "SearchForm")))
            data = serializeCompany(driver, company.get('id'))
            driver.delete_all_cookies()
            print(f"Company #{company.get('id')} scraped!")
            successful.append(data)
        except TimeoutException as te:
            print('Catch timeout...')
            failed.append(company)
        
    return (successful, failed)

def scrape_reviews(driver, wait, reviews):
    successful = []
    failed = []
    print(f'Starting scraping! Total URLs {len(reviews)}')
    for review in reviews:
        try:
            driver.get(review.get('url'))
            wait.until(EC.presence_of_element_located((By.ID, "SearchForm")))
            data = serializeReviews(driver, review.get('id'))
            successful.extend(data)
            driver.delete_all_cookies()
            print(f"Reviews by company #{review.get('id')} scraped!")
        except TimeoutException as te:
            print('Timeout exception')
            failed.append(review)
    return (successful, failed)

def stage_scrape_companies(driver, wait, max_retries=3):
    base_URL = 'https://www.glassdoor.com/Overview/-EI_IE$id.htm?locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    companies_ids = readFromFile('companies_ids.json')
    urls = [{
        "url": base_URL.replace('$id', str(company_id)),
        "id": company_id,
    } for company_id in companies_ids]
    result = []
    while len(urls) and max_retries >= 0:
        successful, urls = scrape_companies(driver, wait, urls)
        result.extend(successful)
        max_retries -= 1
    return result

def stage_scrape_reviews(driver, wait, companies, max_retries=3):
    result = []
    batched_urls = [[{
        "url": company.get('reviews_url').replace('$id', str(company.get('company_id'))).replace('$page', str(page)),
        "id": company.get('company_id'),
    } for page in range(1, floor((company.get('reviews_count') - 1) / 10) + 2)] for company in companies]
    for urls in batched_urls:
        max_retries_temp = max_retries
        while len(urls) and max_retries_temp >= 0:
            successful, urls = scrape_reviews(driver, wait, urls)
            result.extend(successful)
            max_retries_temp -= 1
    
    return result

def commit(companies, reviews):
    for company in companies:
        company_reviews = list(filter(lambda x: x.get('company_id') == company.get('company_id'), reviews))
        company['reviews'] = company_reviews
    return companies
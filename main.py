import time
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from utils import saveToFile
from scrapers import stage_scrape_companies, stage_scrape_reviews, commit

def init_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = uc.Chrome(options=chrome_options)
    driver.set_window_size(1120, 1000)
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 60)
    return (driver, wait)

def main():
    start = time.time()
    driver, wait = init_driver()
    companies = stage_scrape_companies(driver, wait)
    reviews = stage_scrape_reviews(driver, wait, companies)
    result = commit(companies, reviews)
    end = time.time()
    print(f'All is done, total sec - {end-start}')

    saveToFile(result, 'result.json')


if __name__ == '__main__':
    main()
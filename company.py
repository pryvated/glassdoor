from utils import getElementText, getElements, getOnlyNumbers, optionalChaining, saveToFile
from selenium.webdriver.common.by import By

def serialize(driver, company_id):

    appCache = driver.execute_script('return appCache')
    apollo_state = appCache.get('apolloState')
    initial_state = appCache.get('initialState')
    root_query = apollo_state.get('ROOT_QUERY')

    reviews = [value for key, value in root_query.items() if 'employerReviews' in key] if root_query else None
    reviews = [review for review in reviews if 'allReviewsCount' in review] if reviews else None
    employer = [value for key, value in apollo_state.items() if 'Employer:' in key] if apollo_state else None
    employer = employer[0] if employer != None and len(employer) else None
    ceo = [value for key, value in apollo_state.items() if 'Ceo:' in key] if apollo_state else None
    ceo = ceo[0] if ceo != None and len(ceo) else None

    company_name = optionalChaining(employer, ['shortName'])
    company_website = optionalChaining(employer, ['website'])
    company_revenue = optionalChaining(employer, ['revenue'])
    company_headquarters = optionalChaining(employer, ['headquarters'])
    company_size = optionalChaining(employer, ['size'])
    company_ticker = optionalChaining(employer, ['stock'])
    company_ceo_name = optionalChaining(ceo, ['name'])
    company_competitors = optionalChaining(initial_state, ['extractedData', 'pageData', 'competitors'])
    company_competitors = list(map(lambda x: x.get('shortName'), company_competitors))
    reviews_count = optionalChaining(reviews[0], ['allReviewsCount']) if reviews != None and len(reviews) else None
    reviews_url = optionalChaining(employer, ['links', 'reviewsUrl'])
    reviews_url = reviews_url.replace('.htm', '_P$page.htm').replace('/Reviews/', 'https://www.glassdoor.com/Reviews/') if reviews_url else ''

    return {
        "company_id": company_id,
        "company_name": company_name,
        "company_website": company_website,
        "company_revenue": company_revenue,
        "company_headquarters": company_headquarters,
        "company_size": company_size,
        "company_ticker": company_ticker,
        "company_ceo_name": company_ceo_name,
        "company_competitors": company_competitors,
        "reviews_count": reviews_count,
        "reviews_url": reviews_url,
    }
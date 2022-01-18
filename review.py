from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import getElementText, getElements, getOnlyNumbers, optionalChaining

def getReviewResponses(state, review):
    links = review.get('employerResponses')
    result = []
    for link in links:
        ref = optionalChaining(link, ['__ref'])
        result.append({
            "response_text": optionalChaining(state, [ref, 'response']),
            "response_job_title": optionalChaining(state, [ref, 'userJobTitle']),
        })
    return result

def getReviewReviewer(state, review):
    ref = optionalChaining(review, ['jobTitle', '__ref'])
    reviewer_job_title = optionalChaining(state, [ref, 'text'])
    
    return {
        "reviewer_job_title": reviewer_job_title,
        "reviewer_is_current_job": review.get('isCurrentJob'),
        "reviewer_job_ending_year": review.get('jobEndingYear'),
    }

def getReviewDateTime(state, review):
    return review.get('reviewDateTime')

def getReviewLocation(state, review):
    ref = optionalChaining(review, ['location', '__ref'])
    location = optionalChaining(state, [ref, 'name'])
    return location

def getReviewPros(state, review):
    return review.get('pros')

def getReviewCons(state, review):
    return review.get('cons')

def getReviewSummary(state, review):
    return review.get('summary')

def getReviewAdvice(state, review):
    return review.get('advice')

def serialize(driver, company_id):
    state = driver.execute_script('return appCache.apolloState')
    root_query = state.get('ROOT_QUERY')
    reviews = [value for key, value in root_query.items() if 'employerReviews' in key] if root_query else None
    reviews = reviews[0].get('reviews') if reviews != None and len(reviews) else None
    
    return [{
        "company_id": company_id,
        "review_date_time": getReviewDateTime(state, review),
        "review_location": getReviewLocation(state, review),
        "review_reviewer": getReviewReviewer(state, review),
        "review_pros": getReviewPros(state, review),
        "review_cons": getReviewCons(state, review),
        "review_summary": getReviewSummary(state, review),
        "review_advice": getReviewAdvice(state, review),
        "review_employer_responses": getReviewResponses(state, review),
    } for review in reviews] if reviews != None else []
import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))

    try:
        # Call post method of requests library with URL, json payload and parameters
        response = requests.post(url, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:

        # Here we can add further refinement to handle 404 and 500
        #if json_result["code"] != 200:
         #   return results

        reviews = json_result["body"]["data"]
        # For each dealer object
        for review_doc in reviews:
            if dealerId == review_doc.get("dealership"):
            # Create a CarDealer object with values in `doc` object
                review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"], name=review_doc.get("name", ""), car_make=review_doc.get("car_make", "NA"),
                                    car_model=review_doc.get("car_model", "NA"), car_year=review_doc.get("car_year", "NA"), purchase=review_doc.get("purchase", False),
                                    purchase_date=review_doc.get("purchase_date", "NA"), review=review_doc.get("review", ""))
                
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                results.append(review_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    # Call get_request with a URL parameter
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:

        # Here we can add further refinement to handle 404 and 500
        #if json_result["code"] != 200:
         #   return results

        dealers = json_result["body"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            if dealerId == dealer_doc.get("id"):
        
        # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
    
        results.append(dealer_obj.full_name)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    try:
        API_KEY = "nJRnac-aFu5o5YYz8jQXbRxNcAFk2EI9Tt48n7Xw-607"
        URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/231cd2d6-d05c-4c30-9a99-e26dbbf09424"

        authenticator = IAMAuthenticator(API_KEY)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
            )

        natural_language_understanding.set_service_url(URL)

        response = natural_language_understanding.analyze(text=text, features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()

        label = response['sentiment']['document']['label']
        return label
    except Exception as e:
        # If any error occurs
        print("Exception while finding sentiment: {0}".format(e))



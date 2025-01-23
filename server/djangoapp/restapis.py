import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend API base URL (loads from .env file or defaults to localhost)
backend_url = os.getenv('backend_url', default="http://localhost:3030")
# Sentiment analyzer API URL (loads from .env file or defaults to localhost)
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Send a GET request to the backend API with optional query parameters.
    
    Args:
    - endpoint (str): The API endpoint to send the GET request to.
    - kwargs (dict): Optional query parameters for the request.
    
    Returns:
    - dict: JSON response from the API if successful, None if there's an error.
    """
    # Construct the query string from kwargs
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    
    # Construct the full URL for the GET request
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    
    try:
        # Send GET request to the backend API
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an exception for error status codes
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as e:
        # Log any errors and return None
        print(f"Error occurred while making GET request: {e}")
        return None

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of a review using the sentiment analyzer API.
    
    Args:
    - text (str): The review text to analyze.
    
    Returns:
    - dict: Sentiment analysis response from the API.
    """
    # Construct the request URL for sentiment analysis
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"GET to {request_url}")
    
    try:
        # Send GET request to sentiment analyzer
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an exception for error status codes
        return response.json()  # Return JSON response containing sentiment analysis
    except requests.exceptions.RequestException as e:
        # Log any errors and return None
        print(f"Error occurred while analyzing sentiment: {e}")
        return {"error": "An error occurred while analyzing the sentiment."}

def post_review(data_dict):
    """
    Post a review to the backend API.
    
    Args:
    - data_dict (dict): The review data to post to the API.
    
    Returns:
    - dict: The response from the backend after posting the review.
    """
    # Construct the URL for the backend where reviews will be posted
    request_url = f"{backend_url}/insert_review"  # Endpoint for posting the review
    print(f"POST to {request_url}")
    
    try:
        # Send POST request with the review data as JSON
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise an exception for error status codes
        return response.json()  # Return the response as JSON if successful
    except requests.exceptions.RequestException as e:
        # Log any errors and return an error message
        print(f"Error occurred while posting review: {e}")
        return {"error": "An error occurred while posting the review."}

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review  # Import post_review to post reviews

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign-in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    # Try to check if provided credentials can be authenticated
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    else:
        response_data = {"userName": username, "status": "Authentication Failed"}
    
    return JsonResponse(response_data)

@csrf_exempt
def logout_user(request):
    """
    Handle a logout request and return a JSON object with the username set to an empty string.
    """
    # Log out the user
    logout(request)
    # Return a JSON response indicating the user is logged out
    data = {"userName": ""}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    context = {}

    # Parse data from request
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    
    username_exist = False
    email_exist = False
    
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        # Login the user and redirect to the list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)

# Create a `get_cars` view to get a list of cars
def get_cars(request):
    # Count the number of CarMakes in the database
    count = CarMake.objects.filter().count()
    print(count)  # You can remove this line later, it's for debugging

    # If there are no CarMakes, initiate or populate the database (you should define initiate())
    if count == 0:
        initiate()

    # Get all car models, along with the associated car make (using select_related for performance)
    car_models = CarModel.objects.select_related('car_make')
    
    # Create a list of cars with their model and make
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    
    # Return the data as a JSON response
    return JsonResponse({"CarModels": cars})

# Example placeholder function for initiating data if needed (Optional)
def initiate():
    car_make1 = CarMake.objects.create(name="Toyota", description="Japanese car manufacturer")
    car_make2 = CarMake.objects.create(name="Ford", description="American car manufacturer")
    
    CarModel.objects.create(car_make=car_make1, name="Camry", type="SEDAN", year=2023)
    CarModel.objects.create(car_make=car_make2, name="F-150", type="SUV", year=2023)

# Create a `get_dealerships` view to fetch a list of dealerships from an API
def get_dealerships(request, state="All"):
    """
    Fetch dealerships based on the state provided. If "All" is passed, return all dealerships.
    
    Args:
    - state (str): The state to filter dealerships by (default is "All").
    
    Returns:
    - JsonResponse: A JSON response containing the list of dealerships.
    """
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    # Fetch the list of dealerships using the get_request method
    dealerships = get_request(endpoint)
    
    if dealerships:
        return JsonResponse({"status": 200, "dealers": dealerships})
    else:
        return JsonResponse({"status": 500, "error": "Failed to fetch dealerships"})

# Create a `get_dealer_details` view to fetch details of a specific dealer
def get_dealer_details(request, dealer_id):
    """
    Fetch details of a specific dealer based on the dealer_id passed.
    
    Args:
    - dealer_id (str): The unique ID of the dealer to fetch.
    
    Returns:
    - JsonResponse: A JSON response containing the dealer's details.
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{str(dealer_id)}"
        dealership = get_request(endpoint)  # Call the get_request method to fetch dealer details
        
        if dealership:
            return JsonResponse({"status": 200, "dealer": dealership})
        else:
            return JsonResponse({"status": 500, "message": "Failed to fetch dealer details"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request: Dealer ID is required"})

# Create a `get_dealer_reviews` view to fetch reviews of a specific dealer
def get_dealer_reviews(request, dealer_id):
    """
    Fetch reviews for a specific dealer based on the dealer_id passed and analyze their sentiment.
    
    Args:
    - dealer_id (str): The unique ID of the dealer to fetch reviews for.
    
    Returns:
    - JsonResponse: A JSON response containing the dealer's reviews with sentiment analysis.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{str(dealer_id)}"
        reviews = get_request(endpoint)
        
        if reviews:
            # Analyze sentiment for each review and add the sentiment to the review
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail['review'])
                print(response)  # Optional: For debugging purposes
                review_detail['sentiment'] = response['sentiment']
            
            return JsonResponse({"status": 200, "reviews": reviews})
        else:
            return JsonResponse({"status": 500, "error": "Failed to fetch reviews"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request: Dealer ID is required"})

# Create a `add_review` view to allow authenticated users to post a review for a dealer
@csrf_exempt
def add_review(request):
    """
    Handle a POST request for adding a review.
    Ensure the user is authenticated before allowing them to post a review.
    
    Args:
    - request (HttpRequest): The incoming HTTP request.
    
    Returns:
    - JsonResponse: A response containing the status of the review submission.
    """
    if request.user.is_authenticated:  # Check if user is authenticated
        # Parse the review data from the request body
        data = json.loads(request.body)
        
        try:
            # Call the post_review method from restapis.py with the data dictionary
            response = post_review(data)
            print("Post response:", response)  # Optionally print the response for debugging
            
            # Return a success response with status 200
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Exception as e:
            print("Error posting review:", e)  # Print the exception for debugging
            return JsonResponse({"status": 500, "message": "Error in posting review"})
    else:
        # If user is not authenticated, return a 403 Unauthorized response
        return JsonResponse({"status": 403, "message": "Unauthorized"})

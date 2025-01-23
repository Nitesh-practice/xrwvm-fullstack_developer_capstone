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
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign-in request
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

# # Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#    ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request, dealer_id):
#    ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
#    ...

# Create a `add_review` view to submit a review
# def add_review(request):
#    ...

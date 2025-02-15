from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, CarDealer
# from .restapis import related methods
from .restapis import get_request, post_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

BASE_URL = "https://3d5a0256.us-south.apigw.appdomain.cloud/api3/{0}"

# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect("djangoapp:index")

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect("djangoapp:index")
        else:
            # If not, return to login page again
            return redirect("djangoapp:index")
    else:
        return render(request, 'djangoapp/index.html', context)

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://3d5a0256.us-south.apigw.appdomain.cloud/api3/getdealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {'dealership_list': dealerships }
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
    
    #context = {}
    #if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealer_id, dealer_name):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        #url = "https://3d5a0256.us-south.apigw.appdomain.cloud/api3/getreviews"
        reviews = get_dealer_reviews_from_cf("https://3d5a0256.us-south.apigw.appdomain.cloud/api3/review", dealer_id)
        #dealer = get_dealer_by_id_from_cf("https://3d5a0256.us-south.apigw.appdomain.cloud/api3/getdealerships", dealer_id)
        
        context['review_list'] = reviews
        context['dealer'] = dealer_name
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id, dealer_name):
    context = {}

    if request.method == 'GET':
        try:
            context["cars"] = CarModel.objects.filter(dealer_id = dealer_id)
        except:
            return redirect('djangoapp:index')
        context["dealer_id"] = dealer_id
        context["dealer"] = dealer_name
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        time = datetime.utcnow().isoformat(),
        id = int(dealer_id)
        name = request.user.first_name + ' ' + request.user.last_name
        another = ""
        review = request.POST['content']
        purchase_check = request.POST.get('purchasecheck', 'off')
        purchase = True if purchase_check=='on' else False
        purchase_date = request.POST['purchasedate']
        car = CarModel.objects.get(pk = request.POST['car'])
        car_make = car.carmake.name
        car_model = car.modelname
        car_year = car.year
        review = {
            "time": time,
            "id": int(dealer_id),
            "name": name,
            "dealership": int(dealer_id),
            "another": another,
            "review": review,
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car_make": car_make,
            "car_model": car_model,
            "car_year": car_year
        }
        json_payload = {
            "review": review
        }
        response = post_request("https://3d5a0256.us-south.apigw.appdomain.cloud/api3/reviewpost", json_payload)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id, dealer_name=dealer_name)
    else:
        return render(request, 'djangoapp/index.html', context)


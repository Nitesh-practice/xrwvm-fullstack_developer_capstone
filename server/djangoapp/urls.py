from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path('register', views.registration, name='register'),

    # Path for login
    path(route='login', view=views.login_user, name='login'),

    # Path for logout
    path(route='logout', view=views.logout_user, name='logout'),

    # Path for getting cars
    path('get_cars/', views.get_cars, name='get_cars'),

    # Other paths for dealer reviews, add a review, etc.
    # Path for getting dealerships (All or filtered by state)
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # Path for getting details of a specific dealer
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # Path for getting reviews for a specific dealer
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),

    path(route='add_review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

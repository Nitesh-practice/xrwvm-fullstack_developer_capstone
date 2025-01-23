from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.urls import include
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path('register', views.registration, name='register'),

    # Path for login
    path(route='login', view=views.login_user, name='login'),

    # Path for logout
    path(route='logout', view=views.logout_user, name='logout'),

    # Add the path for get_cars
    path('get_cars/', views.get_cars, name='get_cars'),

    # Other paths for dealer reviews, add a review, etc.
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

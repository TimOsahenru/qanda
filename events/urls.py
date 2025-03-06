from django.urls import path
from events import views


urlpatterns = [
    path('', views.home_view, name='home_view'),
]
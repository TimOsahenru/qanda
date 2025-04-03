from django.urls import path
from events import views


urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('event/<slug:slug>/', views.event_details, name='event_details'),
]
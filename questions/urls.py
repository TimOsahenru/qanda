from django.urls import path
from questions import views



urlpatterns = [
    path('ask/<str:slug>/', views.create_question, name='create_question')
]
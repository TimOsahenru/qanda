from django.urls import path
from questions import views



urlpatterns = [
    # path('questions/<str:event_name>/', views.create_question, name='create_questions')
    # path('questions/<str:pk>/', views.create_question, name='create_questions'),
    path('ask/<str:slug>/', views.create_question, name='create_question')
]
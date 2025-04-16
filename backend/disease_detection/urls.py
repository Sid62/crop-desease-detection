from django.urls import path
from .views import predict_disease, get_history, get_disease_details, get_solution

urlpatterns = [
    path('predict/', predict_disease, name='predict_disease'),
    path('history/', get_history, name='get_history'),
    path('disease/<str:disease_name>/', get_disease_details, name='get_disease_details'),
    path('solution/<str:disease_name>/', get_solution, name='get_solution'),
]

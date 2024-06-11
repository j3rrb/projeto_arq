from django.urls import path
from . import views

urlpatterns = [
    path('get-subgroups/', views.get_subgroups, name="Get subgroups")
]

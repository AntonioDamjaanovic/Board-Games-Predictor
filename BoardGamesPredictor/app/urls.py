from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    #path('', views.home, name = 'home_path'),
    path('predict', views.predict, name = 'predict')
]
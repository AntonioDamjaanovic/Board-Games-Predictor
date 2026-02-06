from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    #path('', views.home, name = 'home_path'),
    path('predict', views.predict_view, name = 'predict_view'),
    path('predict/api', views.predict_api, name = 'predict_api'),
]
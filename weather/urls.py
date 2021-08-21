from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('forecast/<str:city>/', views.ForecastView.as_view(), name='forecast')
]
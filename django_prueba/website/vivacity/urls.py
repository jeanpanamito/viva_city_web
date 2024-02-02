from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vista/', views.vista, name='vista'),
    path('vista/upcoming_trips/', views.upcoming_trips, name='upcoming_trips'),
    path('mostrar_destinos/', views.mostrar_destinos, name='mostrar_destinos'),
    path('vista/search/', views.search, name='search'),
    path('travel_destination/', views.travel, name='travel_destination'),
    path('vista/destination_list/<str:country>/', views.destination_list, name='destination_list'),
    path('vista/destination_details/<str:city_name>/', views.vista_destination_details, name='vista_destination_details'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('list/', views.list_view, name='list'),
    path('list/place/', views.place_view, name='place'),
    path('destination_details/<str:city_name>/', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>/pessanger_detail_def/', views.pessanger_detail_def, name='pessanger_detail_def'),
    path('destination_details/<str:city_name>/pessanger_detail_def/card_payment/', views.card_payment, name='card_payment'),
    path('destination_details/<str:city_name>/pessanger_detail_def/net_payment/', views.net_payment, name='net_payment'),
    # Otras rutas...
]



   
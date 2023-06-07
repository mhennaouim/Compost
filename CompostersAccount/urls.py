from django.urls import path
from . import views

urlpatterns = [
    path('CR/', views.composterSignup, name='composterSignup'),
    path('CL/', views.composterLogin, name='composterLogin'),
    path('home/', views.composterHome, name='composterHome'),
    path('getPendingMembres/', views.getPendingMembres, name="getPendingMembres"),
    path('accept_greener/',views.acceptGreener, name='acceptGreener'),
    path('reject_greener/',views.rejectGreener, name='rejectGreener'),
    path('GreenersRequest/', views.getGreenersOffer, name='getGreenersOffer'),
    path('ComposterMembres/', views.getComposterMembers, name='getComposterMembers'),
    path('offers_data/',views.GreenersOffers, name="GreenersOffers"),
    path('logout/', views.logoff , name='logoff'),
]
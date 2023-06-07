from django.urls import path
from . import views

urlpatterns = [
    path('GR/', views.greenerSignup, name='greenerSignup'),
    path('GL/', views.greenerLogin, name='greenerLogin'),
    path('GreenerHomeChooseComposter/', views.greenerHomeChooseComposter, name='greenerHomeChooseComposter'),
    path('GreenerRequestComposterLink/', views.greenerRequestComposterLink, name='greenerRequestComposterLink'),
    path('home/', views.greenerHome, name='greenerHome'),
    path('GreenerNotification', views.greenerNotification, name='greenerNotification'),
    path('offer/', views.compostOffer, name='compostOffer'),
    path('get_closest_composters/', views.getClosestComposters, name='getClosestComposters'),
    path('update_composter/', views.updateComposter, name ='updateComposter'),
    path('logout/', views.logoff , name='logoff'),
    path('checkEmail/', views.checkEmail, name="checkEmail"),
]
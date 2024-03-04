
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.signup,name="register"),
    path('signup/',views.signup,name='signup'),
    path('login/',views.log,name='login'),
    path('',views.tra,name='home'),
    path('SpeechReco/',views.speech_reco,name='SpeechReco'),
    path('tar/',views.tra,name='tar')  
]   

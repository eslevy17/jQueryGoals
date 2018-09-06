from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('success', views.success, name='success'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logoff', views.logoff, name='logoff'),
    path('users/<int:num>', views.user, name='user'),
    
    path('myaccount/<int:num>', views.myaccount, name='myaccount'),
    path('edit_user', views.edit_user, name='edit_user'),
    
    
    path('activities', views.activities, name='activities'),
    path('add_goal', views.add_goal, name='add_goal'),
    path('add_event', views.add_event, name='add_event'),
    path('addToEvent', views.addToEvent, name='addToEvent'),
]
from django.urls import path
from . import views

app_name = 'changed'
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/register/',views.registerUser,name='register'),
    path('signup/',views.signup,name='signup'),
    path('authenticate/',views.auth,name='authenticate'),
    path('logout/',views.logout,name='logout'),
]
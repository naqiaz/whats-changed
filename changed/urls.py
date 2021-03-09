from django.urls import path
from . import views, logic

app_name = 'changed'
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/register/',logic.registerUser,name='register'),
    path('signup/',views.signup,name='signup'),
    path('authenticate/',logic.auth,name='authenticate'),
    path('logout/',logic.logout,name='logout'),
]
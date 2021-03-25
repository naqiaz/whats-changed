from django.urls import path
from . import views, auth

app_name = 'changed'
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/register/',auth.registerUser,name='register'),
    path('signup/',views.signup,name='signup'),
    path('authenticate/',auth.auth,name='authenticate'),
    path('logout/',auth.logout,name='logout'),
    path('review_list/',views.business_review_list,name='reviewlist'),
    path('review_processing/',views.writeReview,name='processreview'),
]
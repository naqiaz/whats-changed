from django.urls import path
from . import views, auth

app_name = 'changed'
urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('signup/register/',auth.registerUser,name='register'),
    path('signup/',views.signup,name='signup'),
    path('authenticate/',auth.auth,name='authenticate'),
    path('logout/',auth.logout,name='logout'),
    path('review_processing/',views.writeReview,name='processreview'),
    path('reviews/',views.show_reviews,name='specificreview'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('replies/<int:id>/',views.reply,name='replies'),
    path('delete_reply/<int:comment_id>/<int:reply_id>',views.delete_reply,name='delete_reply'),
    path('edit_reply/<int:comment_id>/<int:reply_id>',views.edit_reply,name='edit_reply'),
    path('delete_comment/<str:business_pid>/<int:comment_id>',views.delete_comment,name='delete_comment'),
    path('edit_comment/<str:business_pid>/<int:comment_id>',views.edit_comment,name='edit_comment'),
    path('delete_comment_prof/<str:business_pid>/<int:comment_id>',views.delete_comment_prof,name='delete_comment_prof'),
    path('edit_comment_prof/<str:business_pid>/<int:comment_id>',views.edit_comment_prof,name='edit_comment_prof'),
    path('rating/', views.rating, name='rating'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test' ),
    path('get_user/', views.get_user, name='get_user' ),
    path('post/<str:pk>', views.post, name='post' ),
    path('get_user/<str:pk>', views.get_user_by_id, name='get_user_by_id' ),
    path('get_friend_list/<str:pk>', views.get_friend_list, name='get_friend_list' ),

]


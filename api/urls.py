
from django.urls import path
from . import views

urlpatterns = [
    path('get_user/', views.get_user, name='get_user' ),
    path('add_post/', views.add_post, name='add_post' ),
    path('get_all_post/', views.get_all_post, name='get_all_post' ),
    path('signup_step_one/', views.signup_step_one, name='signup_step_one' ),
    path('get_conversation/<str:pk>', views.get_conversation, name='get_conversation' ),
    path('set_online/', views.set_online, name='set_online' ),
    path('get_messages/<str:pk>', views.get_messages, name='get_messages' ),
    path('complet_setup/', views.complet_setup_first_step, name='complet_setup_first_step' ),
    path('complet_setup_images/', views.complet_setup, name='complet_setup' ),
    
    path('post/<str:pk>', views.post, name='post' ),
    path('get_user/<str:pk>', views.get_user_by_id, name='get_user_by_id' ),
    path('get_friend_list/<str:pk>', views.get_friend_list, name='get_friend_list' ),

]


from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment/<int:wall_message_id>', views.post_comment),
]

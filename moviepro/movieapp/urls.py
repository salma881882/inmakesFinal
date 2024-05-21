from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),

    path('register', views.register, name="register"),

    path('my_login', views.my_login, name="my_login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user_logout', views.user_logout, name="user_logout"),

    path('add_movie', views.add_movie, name="add_movie"),

    path('detail/<int:movie_id>/', views.detail, name='detail'),

    path('update/<int:id>/', views.update, name='update'),

    path('delete/<int:id>/', views.delete, name='delete'),

]

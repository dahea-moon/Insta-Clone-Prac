from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('singup/', views.signup, name='singup'),
    path('login/', views.login, name='logtin'),
    path('logout/', views.logout, name='logout'),
    path('userpage/<int:user_id>/', views.user_page, name='user_page'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
]

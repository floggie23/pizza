from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('order/add', views.orderadd),
    path('order/create', views.createorder),
    path('purchase/<str:id>', views.purchase),
    path('user/edit', views.edit),
    path('user/update', views.update),
    path('favorite/remove/<str:id>', views.removefavorite),
    path('favorite/add/<str:id>', views.addfavorite),
    path('favorite/delete/<str:id>', views.deletefavorite),
    path('randompizza', views.createRandom),

]
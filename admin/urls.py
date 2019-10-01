from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('product', views.product, name="product"),
    path('addProduct', views.addProduct, name="addproduct"),
    path('user', views.user, name="user"),
    path('addUser', views.addUser, name="addUser"),
    path('logout', views.logout, name="logout")
]

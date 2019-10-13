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
    path('customer', views.customer, name="customer"),
    path('addCustomer', views.addCustomer, name="addCustomer"),
    path('viewCustomer/<int:id>', views.viewCustomer, name="viewCustomer"),
    path('deleteCustomer/<int:id>', views.deleteCustomer, name="deleteCustomer"),
    path('render_pdf_view', views.render_pdf_view, name="render_pdf_view"),
    path('logout', views.logout, name="logout")
]

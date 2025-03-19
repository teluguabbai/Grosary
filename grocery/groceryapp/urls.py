from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Default Django login redirect (/accounts/login/)
    path('accounts/login/', auth_views.LoginView.as_view(), name='default_login'),

    # Cart-related URLs
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    
    path("payment/", views.payment, name="payment"),
    path("order-success/", views.order_success, name="order_success"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add-product/", views.add_product, name="add_product"),
    path("delete-product/<int:product_id>/", views.delete_product, name="delete_product"),
    path("checkout/", views.checkout, name="checkout"),
    path("cod_payment/", views.cod_payment, name="cod_payment"),
    path('profile/', views.profile_view, name='profile'),
    path("update-address/", views.update_address, name="update_address"),
    

    
]

# Handle media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from .views import admin_dashboard, add_product


from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('account/', views.account, name='account'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_product_from_cart/<int:product_id>/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('acoustics/', views.acoustics, name='acoustics'),
    path('solid/', views.solid, name='solid'),
    path('hollow/', views.hollow, name='hollow'),
]

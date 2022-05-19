from django.urls import path, re_path
from . import views 
app_name="Ehub"
urlpatterns = [
    path('', views.Home.as_view(), name="home-view"),
    path('your-cart',views.UserCartView.as_view(),name="your-cart"),
    path('search/', views.SearchEngineView.as_view(), name="search-engine-view"),
    path('checkout/', views.CheckoutView.as_view(), name='checkout-view'),

]

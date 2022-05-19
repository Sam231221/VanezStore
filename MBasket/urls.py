from django.urls import path
from . import views
app_name = 'Basket'

urlpatterns = [

    path('add/', views.BasketAddView.as_view(), name='basket-add-view'),
    path('update/', views.BasketUpdateView.as_view(), name='basket-update-view'),
    path('delete/', views.BasketDeleteView.as_view(), name='basket-delete-view'),
    path('delvieryoptions/', views.BasketDeliveryView.as_view(), name='basket-delivery-view'),
    
]
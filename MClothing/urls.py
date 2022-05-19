from django.urls import path, re_path
from . import views 
app_name="Clothes"
urlpatterns = [

   path('product_json_view/', views.ProductJsonView.as_view(), name='product-json-view'),
   path('store/',views.StoreView.as_view() , name="store"),
   path('products_filtered_json_view/',views.ProductFilterJsonView.as_view() , name="products-filter-json-view"),
   path('products_review_json_view/<int:pid>/',views.ProductReviewJsonView.as_view() , name="product-review-json-view"),
   path('load_more_view/',views.LoadMoreView.as_view() , name="load-more-view"),
    path('product_detail/<str:slug>/', views.ProductDetailView.as_view(), name="product-detail-view"),
    
]

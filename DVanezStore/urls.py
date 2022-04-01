from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('MClothing.urls', namespace="Clothes")),
    path('',include('MBasket.urls', namespace="basket")),
]

#for acessing media url
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
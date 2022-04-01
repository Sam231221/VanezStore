from .models import Category, Product
from django.db.models import Min,Max
def categories(request):
    return {'categories': Category.objects.all()}


def get_filters(request):
	minMaxPrice=Product.objects.aggregate(Min('price'),Max('price'))
	return {'minMaxPrice':minMaxPrice}
from multiprocessing import context
from django.shortcuts import render
from django.views.generic import TemplateView, View
from MClothing.models import Product
from django.http.response import JsonResponse
from MBasket.basket import Basket
from .models import DeliveryOptions
class Home(TemplateView):
    template_name = 'frontendbase.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featuredproducts"] = Product.products.filter(is_featured=True).order_by('-id')[:4]
        context["recentproducts"] = Product.products.all().order_by('-published_on')[:4]
        
        return context

'''
    def get(self, request):
        context={
                "featuredproducts": Product.products.filter(is_featured=True).order_by('-id')[:4],
                "recentproducts" : Product.products.all().order_by('-published_on')[:4],
        }    
        return JsonResponse({'data':True}, safe=False)
'''

class SearchEngineView(View):
    def post(self, request):
        query = request.POST['keyword']
        print(query)
        product_queryset =  Product.products.filter(title__icontains=query)
        print(product_queryset)
        if len(product_queryset) > 0 and len(query) > 0:
            product_list = [] #inititae an empty list
            
            #Append all customer obj into the list using loop.
            for obj in product_queryset:
                item= {
                    'pk': obj.id,
                    'url': obj.get_absolute_url(),
                    'title': obj.title 
                }
                product_list.append(item)
            
            #now attach customer_list  to the response
            response = product_list    
        else:
            response = "Sorry, We don't currently have "+str(query)    
            print(response)        
        
        return JsonResponse({'queryset':response}, safe=False)
        

class UserCartView(View):
    def get(self, request):
        basket = Basket(request)
        print('Total price:',basket.get_subtotal_price())
        return render(request, 'your-cart.html', {'basket': basket})


class CheckoutView(View):
    def get(self,request):
        context={
            'deliveryoptions':DeliveryOptions.objects.all()
        }
        return render(request, 'checkout.html', context)
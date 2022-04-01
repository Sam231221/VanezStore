import json
from turtle import title
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from .models import Color, Product, Category, Customer, Size
from django.template.loader import render_to_string

class Home(TemplateView):
    template_name = 'frontendbase.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featuredproducts"] = Product.products.filter(is_featured=True).order_by('-id')[:4]
        context["recentproducts"] = Product.products.all().order_by('-published_on')[:4]
        
        return context
   
class ProductJsonView(View):
    def post(self, request):
        data = json.loads(request.body)
        prod_id = data['prod_id']
        prod_code = data['prod_code']
        prod_obj = Product.objects.get(id=prod_id, product_code=prod_code)#type class
        images =  prod_obj.imagealbum_set.all()

        products_dict = {
            'id' : prod_obj.id,
            'name' : prod_obj.title,
            'description' : prod_obj.description,
            'price': prod_obj.price,
            'thumbnail':prod_obj.thumbnail,
            'images':images
        }
        images_list = list(prod_obj.imagealbum_set.values())
        products_dict['images']=images_list
        return JsonResponse(products_dict, safe=False)
    
class ProductDetailView(View):
    def get(self, request):
        return render('product-detail.html') 

class StoreView(View):
    def get(self, request):
        category_queryset = Category.objects.all()
        product_queryset = Product.products.all().order_by('?')[:6]
            
        context={
            'categories': category_queryset,
            'products': product_queryset,
            'limitedproducts': product_queryset.count(),
            'totalproducts':Product.objects.count(),
            'sizes':Size.objects.all(),
            'colors':Color.objects.all()
        }
        return render(request, 'store.html', context)

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
        
            

class ProductFilterJsonView(View):
    def get(self, request):
        colors = request.GET.getlist('color[]')
        sizes = request.GET.getlist('size[]')
        categories = request.GET.getlist('category[]')
        minPrice = request.GET['minPrice']
        maxPrice = request.GET['maxPrice']

        product_queryset = Product.products.filter(price__gte=minPrice, price__lte=maxPrice).order_by("?")
        print('QuerySet:',product_queryset)

        if len(colors) >0:
            #one product can contain more than one colour so use distinct() for single unique obj.
           product_queryset = product_queryset.filter(color__id__in=colors).distinct()

        if len(categories)>0:
            product_queryset=product_queryset.filter(category__id__in=categories).distinct()
       
        if len(sizes)>0:
            product_queryset=product_queryset.filter(size__id__in=sizes).distinct()        
        
        html = render_to_string('utilities/productsbyfilter.html',{'products':product_queryset})
        return JsonResponse({'products': html})
    

class LoadMoreView(View):
    def get(self, request):
        offset=int(request.GET['offset'])
        limit=int(request.GET['limit'])
        product_queryset =Product.products.all().order_by('-published_on')[offset:offset+limit]
        html = render_to_string('utilities/productsbyfilter.html',{'products':product_queryset})
        return JsonResponse({'products': html})




import json
from django.db.models import Avg
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Color, Product, Category, Customer, Size, ProductReview
from django.template.loader import render_to_string
from .forms import ReviewAddForm
from django.contrib.auth.models import User

class StoreView(View):
    def get(self, request):
        
        category_queryset = list(Category.objects.values())
        for category in category_queryset:
            print(category)
            category['product_count'] = Product.objects.filter(category=Category.objects.filter(name=category['name']).first()).count()
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
   
   
class ProductDetailView(View):
    def get(self, request,slug):
        product=Product.products.filter(slug=slug).first()
        reviewForm=ReviewAddForm()
        canAdd=True
        if request.user.is_authenticated:
            
            user_obj = User.objects.get(username=str(request.user))
            reviewCheck=ProductReview.objects.filter(user=user_obj,product=product).count()
            
            if reviewCheck > 0:
                canAdd=False
        else:
            canAdd=True

        reviews=ProductReview.objects.filter(product=product)
        avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
        context={'i':product,
                 'reviewForm':reviewForm,
                 'canAdd':canAdd,
                 'reviews':reviews,
                 'avg_reviews':avg_reviews}
            
        return render(request,'productdetail.html', context)    
   
   
class ProductJsonView(View):
    def post(self, request):
        data = json.loads(request.body)
        prod_id = data['prod_id']
        prod_code = data['prod_code']
        prod_obj = Product.objects.get(id=prod_id, product_code=prod_code)#type class
        print(prod_obj)
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
    
    
class ProductReviewJsonView(View):
    def post(self,request,pid):
        product=Product.products.get(pk=pid)
        user_obj = User.objects.get(username=str(request.user))
        ProductReview.objects.create(
            user=user_obj,
            product=product,
            review_text=request.POST['review_text'],
            review_rating=request.POST['review_rating'],)
        data={
            'user':user_obj.username,
            'review_text':request.POST['review_text'],
            'review_rating':request.POST['review_rating']
        }

        # Fetch avg rating for reviews
        avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
        return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews},safe=False)

      
class ProductFilterJsonView(View):
    def get(self, request):
        colors = request.GET.getlist('color[]')
        sizes = request.GET.getlist('size[]')
        print('sizes:', len(sizes))
        categories = request.GET.getlist('category[]')
        print(categories, sizes, colors)
        minPrice = request.GET['minPrice']
        maxPrice = request.GET['maxPrice']

        product_queryset = Product.products.filter(price__gte=minPrice, price__lte=maxPrice).order_by("?")
        print('\n BeforeQuerySet:',product_queryset)

        if len(colors) >0:
            #one product can contain more than one colour so use distinct() for single unique obj.
           product_queryset = product_queryset.filter(color__id__in=colors).distinct()

        if len(categories)>0:
            product_queryset=product_queryset.filter(category__id__in=categories).distinct()
       
        if len(sizes)>0:
            product_queryset=product_queryset.filter(size__id__in=sizes).distinct() 

        print('\n After QuerySet:',product_queryset)
        html = render_to_string('utilities/productsbyfilter.html',{'products':product_queryset})
        return JsonResponse({'products': html})
    

class LoadMoreView(View):
    def get(self, request):
        offset=int(request.GET['offset'])
        limit=int(request.GET['limit'])
        product_queryset =Product.products.all().order_by('-published_on')[offset:offset+limit]
        html = render_to_string('utilities/productsbyfilter.html',{'products':product_queryset})
        return JsonResponse({'products': html})




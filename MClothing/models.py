from random import randrange
from django.conf import settings
from django.utils import timezone
from django.db import models
import datetime
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth.models import User

CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
LENGTH = 16
MAX_TRIES = 32


class Category(models.Model):
    name = models.CharField(max_length = 20,db_index=True, unique=True, null=True)
    slug = models.SlugField(max_length= 50, null=True, blank=True)
    date_added = models.DateTimeField(null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Size(models.Model):
    name = models.CharField(max_length = 20,db_index=True, unique=True, null=True)
    slug = models.SlugField(max_length= 50, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Size, self).save(*args, **kwargs)    
    

class Color(models.Model):
    name = models.CharField(max_length = 20,db_index=True, unique=True, null=True)
    slug = models.SlugField(max_length= 50, null=True, blank=True)
    color_code=models.CharField(max_length=100, null=True)

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))
        
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Color, self).save(*args, **kwargs)    

class Customer(models.Model):
    name = models.CharField(max_length=128, null=True)  #test_data
    email = models.EmailField(null= True)
    code = models.CharField(max_length=LENGTH, editable=False, unique=True)
    publish_date = models.DateField(default = datetime.date.today)  
    last_updated=models.DateTimeField(default=timezone.now)    
    
    class Meta:
            ordering = ('-name',)

    def __unicode__(self):
        return "%s: %s" % (self.code, self.name)

    def __str__(self):
        return "%s" % (self.name)


    def save(self, *args, **kwargs):
        loop_num = 0
        unique = False
        while not unique:
            if loop_num < MAX_TRIES:
                new_code = ''
                for i in range(LENGTH): #change to xrange() for python 2
                    new_code += CHARSET[randrange(0, len(CHARSET))]
                if not Customer.objects.filter(code=new_code):
                    self.code = new_code
                    unique = True
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")
        super(Customer, self).save(*args, **kwargs)


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


 
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.SET_NULL, null= True, blank=True)
    title = models.CharField(null=True,db_index=True, max_length=50)
    author = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(null = True)
  
    
    slug = models.SlugField(max_length=50)
    product_code = models.CharField(max_length=LENGTH, editable=False, unique=True, null= True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, help_text="if set active, then it will be visible in the website.")
    published_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-title',)

    def image(self):
        return mark_safe('<img style="object-fit:contain;" src="%s" width="50" height="50" />' % (self.thumbnail))

    def __str__(self):
        return self.title
   
    def save(self, *args, **kwargs):
        loop_num = 0
        unique = False
        while not unique:
            if loop_num < MAX_TRIES:
                new_code = ''
                for i in range(LENGTH): #change to xrange() for python 2
                    new_code += CHARSET[randrange(0, len(CHARSET))]
                    print('sdasda',new_code)
                if not Product.objects.filter(product_code=new_code):
                    self.product_code = new_code
                    unique = True
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")
        
        self.slug=slugify(self.title)      
        super(Product, self).save(*args, **kwargs)    
        
    def get_absolute_url(self):
        return reverse("Clothes:product-detail-view", kwargs={"slug":self.slug})
         
                    
class ImageAlbum(models.Model):
    image = models.URLField(null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,
                                help_text='Provide a url of image',
                                null=True,verbose_name="Images")

              
# Product Review
RATING=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    review_text=models.TextField(null=True)
    review_rating=models.CharField(choices=RATING,max_length=150, null=True)

    class Meta:
        verbose_name_plural='Reviews'


    def __str__(self):
        return f"Reviewed By {self.user}"        
    
    def get_review_rating(self):
        return self.review_rating
    
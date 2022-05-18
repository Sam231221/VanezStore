from django.test import TestCase
from django.contrib.auth import get_user_model
from MClothing.models import Category, Product, Customer
from django.urls import reverse

class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = Customer.objects.create(
            name='Sam',
            email = 'samirshahi9882@gmail.com'
            )
        self.category = Category.objects.create(
            name='Men'
        )
        self.product = Product.objects.create(
            category = self.category,
            title ='Jacket',
            price = 34,
            author = self.user
        )
    
    def test_customer_attributes(self):
        user_obj  = self.user
        self.assertEqual(f'{user_obj.name}','Sam')   
        self.assertEqual(f'{user_obj.email}','samirshahi9882@gmail.com')  
        
    def test_product_attributes(self):
        self.assertEqual(f'{self.product.title}','Jacket')   
        self.assertEqual(f'{self.product.price}','34')  


class HomeViewTest(TestCase):
    def testview_home_url(self):
        route=self.client.get('/')
        self.assertEqual(route.status_code, 200)  # check if route's status code is 200,
        
    def testview_url_by_name(self):
        route = self.client.get(reverse('home'))
        self.assertEqual(route.status_code, 200)
        
    def testview_uses_correct_template(self):
        route = self.client.get(reverse('home'))
        self.assertEqual(route.status_code, 200)      
        self.assertTemplateUsed(route, 'frontendbase.html')   # check if route is using frontendbase.html


class TestCategory(TestCase):
    def setUp(self):
        self.cat_obj1 = Category.objects.create(name="Sameer")
        
    def test_content(self):
        category_obj = self.cat_obj1
        exepected_name = f'{category_obj.name}'
        self.assertEqual(exepected_name,'Sameer')  #check if category with id 1 has name 'Sameer'
        self.assertTrue(isinstance(category_obj,Category))

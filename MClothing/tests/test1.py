from django.test import TestCase
from django.contrib.auth import get_user_model
from MClothing.models import Category, Product, Customer
from django.urls import reverse


class TestCategory(TestCase):
    def setUp(self):
        self.cat_obj1 = Category.objects.create(name="Sameer")
        
    def test_content(self):
        category_obj = self.cat_obj1
        exepected_name = f'{category_obj.name}'
        self.assertEqual(exepected_name,'Sameer')  #check if category with id 1 has name 'Sameer'
        self.assertTrue(isinstance(category_obj,Category))

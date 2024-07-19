from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Product


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('product-list')

    def test_create_product(self):
        response = self.client.post(self.url, self.example_data, format='json')
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        # self.assertEqual(Product.objects.get().pk)

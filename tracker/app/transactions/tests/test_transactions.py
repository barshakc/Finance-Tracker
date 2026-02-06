from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from transactions.models import Transaction, Category
from datetime import datetime

User = get_user_model()

class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category_food = Category.objects.create(name='Food')

        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {self.token}")

class TransactionTests(BaseTestCase):
    def test_create_transaction(self):
        data = {
            "transaction_type": "EXPENSE",
            "amount": 50.0,
            "category": "Food",
            "description": "Lunch",
            "date": datetime.now().isoformat(),
        }
        response = self.client.post(reverse("transaction-list"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
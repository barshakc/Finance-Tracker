from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from transactions.models import Transaction, Category
from django.utils import timezone

User = get_user_model()

class DashboardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category_food = Category.objects.create(name="Food")

        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        Transaction.objects.create(
            user=self.user,
            transaction_type="EXPENSE",
            amount=100,
            category=self.category_food,
            date=timezone.now()
        )
        Transaction.objects.create(
            user=self.user,
            transaction_type="INCOME",
            amount=500,
            date=timezone.now()
        )

    def test_dashboard_response(self):
        response = self.client.get(reverse("transaction-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("monthly", response.data)
        self.assertIn("yearly", response.data)

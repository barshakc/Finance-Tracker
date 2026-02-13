from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from transactions.models import Budget, Category

User = get_user_model()


class BaseBudgetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="budgetuser", password="budgetpass"
        )
        self.category_food = Category.objects.create(name="Food")

        response = self.client.post(
            reverse("login"),
            {"username": "budgetuser", "password": "budgetpass"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


class BudgetTests(BaseBudgetTestCase):
    def test_create_budget_success(self):
        data = {
            "category": "Food",
            "limit_amount": 500,
            "period": "MONTHLY",
            "start_date": timezone.now().date(),
            "end_date": (timezone.now() + timedelta(days=30)).date(),
            "is_active": True,
        }

        response = self.client.post(reverse("budget-list"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Budget.objects.count(), 1)

    def test_create_budget_overlap_failure(self):

        Budget.objects.create(
            user=self.user,
            category=self.category_food,
            limit_amount=300,
            period="MONTHLY",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
        )

        data = {
            "category": "Food",
            "limit_amount": 200,
            "period": "MONTHLY",
            "start_date": timezone.now().date(),
            "end_date": (timezone.now() + timedelta(days=15)).date(),
            "is_active": True,
        }

        response = self.client.post(reverse("budget-list"), data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("active budget for this category", str(response.data))

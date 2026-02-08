from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from transactions.models import Transaction, Category, Budget

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
        self.assertIn("kpis", response.data)

    def test_dashboard_kpis(self):
        Budget.objects.create(
            user=self.user,
            category=self.category_food,
            limit_amount=200,
            period="MONTHLY",
            is_active=True,
        )

        response = self.client.get(reverse("transaction-dashboard"))
        self.assertEqual(response.status_code, 200)

        kpis = response.data.get("kpis")
        self.assertIsNotNone(kpis)

        # KPI calculations
        income_total = Transaction.objects.filter(
            user=self.user, transaction_type="INCOME"
        ).aggregate(total=Sum("amount"))["total"] or 0

        expense_total = Transaction.objects.filter(
            user=self.user, transaction_type="EXPENSE"
        ).aggregate(total=Sum("amount"))["total"] or 0

        net_savings = income_total - expense_total

        total_budget = Budget.objects.filter(
            user=self.user, is_active=True
        ).aggregate(total=Sum("limit_amount"))["total"] or 0

        budget_used_percentage = round((expense_total / total_budget) * 100, 2) if total_budget > 0 else 0

        self.assertEqual(kpis["total_income"], float(income_total))
        self.assertEqual(kpis["total_expense"], float(expense_total))
        self.assertEqual(kpis["net_savings"], float(net_savings))
        self.assertEqual(kpis["budget_used_percentage"], budget_used_percentage)

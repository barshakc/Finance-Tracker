import io
import pandas as pd
from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from transactions.models import Transaction, Category

User = get_user_model()


class BaseUploadTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="uploaduser", password="uploadpass"
        )
        self.category_food = Category.objects.create(name="Food")

        response = self.client.post(
            reverse("login"),
            {"username": "uploaduser", "password": "uploadpass"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


class UploadFileTests(BaseUploadTestCase):
    def test_upload_csv_file_success(self):

        df = pd.DataFrame(
            {
                "transaction_type": ["EXPENSE", "INCOME"],
                "amount": [20, 200],
                "category": ["Food", ""],
                "description": ["Coffee", "Salary"],
                "date": [timezone.now(), timezone.now()],
            }
        )
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        csv_file.seek(0)
        csv_file.name = "transactions.csv"

        response = self.client.post(
            reverse("transaction-upload-file"), {"file": csv_file}, format="multipart"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("transactions imported successfully", response.data["message"])
        self.assertEqual(Transaction.objects.count(), 2)

    def test_upload_invalid_file_type(self):

        text_file = io.StringIO("Not a CSV")
        response = self.client.post(
            reverse("transaction-upload-file"), {"file": text_file}, format="multipart"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported file type", response.data["error"])

    def test_upload_no_file(self):
        response = self.client.post(
            reverse("transaction-upload-file"), {}, format="multipart"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file uploaded", response.data["error"])

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES =[
        ("admin","Admin"),
        ("user","User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")


class Category(models.Model):
    name = models.CharField(max_length=50,unique= True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
        ("SAVINGS", "Savings"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['user','date','transaction_type']),
            models.Index(fields=["user", "category", "transaction_type", "date"]),
            
        ]

    def clean(self):
        if self.transaction_type == "EXPENSE" and not self.category:
            raise ValidationError("Expense transactions must have a category.")
        if self.transaction_type != "EXPENSE" and self.category:
            raise ValidationError("Only expense transactions can have a category.")

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"


class Budget(models.Model):
    PERIOD_CHOICES = [
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
        ("WEEKLY", "Weekly"),
        ("CUSTOM", "Custom"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budgets"
    )
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "period", "start_date", "end_date"],
                name="unique_budget_per_period",
            )
        ]

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.limit_amount})"

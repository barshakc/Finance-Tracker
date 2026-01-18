from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('SAVINGS', 'Savings'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField (max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.type == 'expense' and not self.category:
            raise ValidationError("Expense transactions must have a category.")
        if self.type != 'expense' and self.category:
            raise ValidationError(f"{self.type.capitalize()} transactions should not have a category.")
        

class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"
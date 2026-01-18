from rest_framework import serializers
from .models import Transaction, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'amount', 'category', 'description', 'date']
        read_only_fields = ['user', 'date']

    def validate(self, data):
        transaction_type = data.get('transaction_type')
        category = data.get('category')

        if transaction_type == 'EXPENSE' and category is None:
            raise serializers.ValidationError("Expense transactions must have a category.")
        if transaction_type != 'EXPENSE' and category is not None:
            raise serializers.ValidationError(f"{transaction_type.capitalize()} transactions should not have a category.")

        return data
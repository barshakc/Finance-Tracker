from rest_framework import serializers
from .models import Transaction, Category, Budget
from django.db.models import Sum


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "user", "transaction_type", "amount", "category", "description", "date"]
        read_only_fields = ["user"]

    def validate(self, data):
        transaction_type = data.get("transaction_type")
        category = data.get("category")

        if transaction_type == "EXPENSE" and category is None:
            raise serializers.ValidationError("Expense transactions must have a category.")
        if transaction_type != "EXPENSE" and category is not None:
            raise serializers.ValidationError("Only expense transactions can have a category.")

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "category", "limit_amount", "period", "start_date", "end_date", "is_active", "created_at", "updated_at"]

    def validate(self, attrs):
        user = self.context["request"].user

        qs = Budget.objects.filter(
            user=user,
            category=attrs["category"],
            start_date__lte=attrs["end_date"],
            end_date__gte=attrs["start_date"],
            is_active=True,
        )
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("An active budget for this category and period already exists.")
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BudgetReadSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ["id", "category", "limit_amount", "period", "start_date", "end_date", "is_active", "created_at", "updated_at", "spent_amount", "remaining_amount", "percentage_used"]

    def get_spent_amount(self, obj):
        if not hasattr(obj, "_spent_cache"):
            obj._spent_cache = (
                Transaction.objects.filter(
                    user=obj.user,
                    category=obj.category,
                    transaction_type="EXPENSE",
                    date__range=[obj.start_date, obj.end_date]
                ).aggregate(total=Sum("amount"))["total"] or 0
            )
        return obj._spent_cache

    def get_remaining_amount(self, obj):
        return obj.limit_amount - self.get_spent_amount(obj)

    def get_percentage_used(self, obj):
        spent = self.get_spent_amount(obj)
        return round((spent / obj.limit_amount) * 100, 2) if obj.limit_amount > 0 else 0

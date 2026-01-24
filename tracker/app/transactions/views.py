from rest_framework import serializers, generics, viewsets, filters
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from calendar import month_name
from rest_framework.response import Response
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction, Category, Budget
from .serializers import (
    TransactionSerializer,
    CategorySerializer,
    BudgetSerializer,
    BudgetReadSerializer,
)
from .permissions import IsAdmin, IsOwnerOrAdmin

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Category.objects.all()
        return Category.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["category", "transaction_type"]
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def monthly_expense(request):
    user = request.user
    qs = (
        Transaction.objects.filter(user=user, transaction_type="EXPENSE")
        .annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total_amount=Sum("amount"))
        .order_by("month")
    )
    data = {month_name[int(item["month"])]: float(item["total_amount"]) for item in qs}
    return Response(data)


class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["category", "period", "is_active"]
    ordering_fields = ["start_date", "limit_amount"]
    ordering = ["-start_date"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Budget.objects.all()
        return Budget.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BudgetReadSerializer
        return BudgetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

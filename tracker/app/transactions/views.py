from rest_framework import serializers, generics, viewsets, filters
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from collections import defaultdict

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
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save()  

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


    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        if not transactions.exists():
            return Response({
                "monthly": {"expenses": {}, "income": {}},
                "yearly": {"expenses": {}, "income": {}},
            })

        def monthly_aggregation(trans_type):
            qs = (
                transactions
                .filter(transaction_type=trans_type)
                .annotate(month=TruncMonth("date"))
                .values("month")
                .annotate(total=Sum("amount"))
                .order_by("month")
            )

            data = defaultdict(float)
            for item in qs:
                label = item["month"].strftime("%b")  
                data[label] += float(item["total"])
            return data
        
        def yearly_aggregation(trans_type):
            qs = (
                transactions
                .filter(transaction_type=trans_type)
                .annotate(year=TruncYear("date"))
                .values("year")
                .annotate(total=Sum("amount"))
                .order_by("year")
            )

            data = defaultdict(float)
            for item in qs:
                label = str(item["year"].year)  # 2026
                data[label] += float(item["total"])
            return data

        return Response({
            "monthly": {
                "expenses": monthly_aggregation("EXPENSE"),
                "income": monthly_aggregation("INCOME"),
            },
            "yearly": {
                "expenses": yearly_aggregation("EXPENSE"),
                "income": yearly_aggregation("INCOME"),
            },
        })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def monthly_expense(request):
    user = request.user
    qs = (
        Transaction.objects.filter(user=user, transaction_type="EXPENSE")
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total_amount=Sum("amount"))
        .order_by("month")
    )
    data = {item["month"].strftime("%B %Y"): float(item["total_amount"]) for item in qs}
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
        serializer.save()

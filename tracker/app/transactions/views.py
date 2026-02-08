from rest_framework import serializers, generics, viewsets, filters
import pandas as pd
import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from collections import defaultdict

from .models import Transaction, Category, Budget
from .serializers import (
    TransactionSerializer,
    CategorySerializer,
    BudgetSerializer,
    BudgetReadSerializer,
    RegisterSerializer,
    DashboardSerializer,
    UploadFileResponseSerializer,
    LoginRequestSerializer,
    LoginResponseSerializer,
)

from .permissions import IsAdmin, IsOwnerOrAdmin
from transactions.etl.transform import transform_transaction

logger = logging.getLogger(__name__)
User = get_user_model()


@extend_schema(
    request=RegisterSerializer,
    responses={201: RegisterSerializer},
    description="Register a new user",
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(
    request=LoginRequestSerializer,
    responses={200: LoginResponseSerializer},
    description="Login and obtain JWT access and refresh tokens",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    description="Retrieve, create, update, or delete categories",
    responses={200: CategorySerializer},
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["category", "transaction_type"]
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"file": {"type": "string", "format": "binary"}},
            }
        },
        responses={200: UploadFileResponseSerializer},
        description="Upload CSV or Excel file to bulk import transactions",
    )
    @action(detail=False, methods=["post"], url_path="upload")
    def upload_file(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)
            else:
                return Response({"error": "Unsupported file type"}, status=400)

            from transactions.etl.transform import transform_transaction

            df = transform_transaction(df)

            transactions = []
            for _, row in df.iterrows():
                category_name = (
                    str(row["category"]).strip()
                    if pd.notna(row["category"]) and str(row["category"]).strip() != ""
                    else "Miscellaneous"
                )
                category_obj, _ = Category.objects.get_or_create(name=category_name)

                transactions.append(
                    Transaction(
                        user=request.user,
                        transaction_type=row["transaction_type"],
                        amount=row["amount"],
                        category=category_obj,
                        description=row.get("description"),
                        date=row["date"],
                    )
                )

            with transaction.atomic():
                Transaction.objects.bulk_create(transactions)

            return Response(
                {"message": f"{len(transactions)} transactions imported successfully"}
            )

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @extend_schema(
        responses={200: DashboardSerializer},
        description="Returns KPI cards, monthly and yearly analytics for expenses, income, and budgets",
    )
    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        income_total = (
            transactions.filter(transaction_type="INCOME").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        expense_total = (
            transactions.filter(transaction_type="EXPENSE").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        net_savings = income_total - expense_total

        total_budget = (
            Budget.objects.filter(user=user, is_active=True).aggregate(
                total=Sum("limit_amount")
            )["total"]
            or 0
        )

        budget_used_percentage = (
            round((expense_total / total_budget) * 100, 2) if total_budget > 0 else 0
        )

        kpis = {
            "total_income": float(income_total),
            "total_expense": float(expense_total),
            "net_savings": float(net_savings),
            "budget_used_percentage": budget_used_percentage,
        }

        if not transactions.exists():
            return Response(
                {
                    "kpis": kpis,
                    "monthly": {"expenses": {}, "income": {}, "budget": []},
                    "yearly": {"expenses": {}, "income": {}, "budget": []},
                }
            )

        def aggregate(trans_type, period):
            qs = transactions.filter(transaction_type=trans_type)

            if period == "monthly":
                qs = qs.annotate(p=TruncMonth("date"))
            else:
                qs = qs.annotate(p=TruncYear("date"))

            qs = qs.values("p").annotate(total=Sum("amount")).order_by("p")

            data = defaultdict(float)
            for item in qs:
                label = (
                    item["p"].strftime("%b")
                    if period == "monthly"
                    else str(item["p"].year)
                )
                data[label] += float(item["total"])
            return data

        def get_budgets(period):
            period_map = {"monthly": "MONTHLY", "yearly": "YEARLY"}
            db_period = period_map.get(period.lower(), period.upper())

            return [
                {
                    "category": b.category.name,
                    "limit_amount": float(b.limit_amount),
                }
                for b in Budget.objects.filter(
                    user=user, period=db_period, is_active=True
                )
            ]

        return Response(
            {
                "kpis": kpis,
                "monthly": {
                    "expenses": aggregate("EXPENSE", "monthly"),
                    "income": aggregate("INCOME", "monthly"),
                    "budget": get_budgets("monthly"),
                },
                "yearly": {
                    "expenses": aggregate("EXPENSE", "yearly"),
                    "income": aggregate("INCOME", "yearly"),
                    "budget": get_budgets("yearly"),
                },
            }
        )


@extend_schema(responses={200: dict}, description="Get monthly total expenses per user")
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


@extend_schema(
    description="Manage budgets: create, list, update, delete",
    responses={200: BudgetReadSerializer},
)
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

from django.urls import path, include
from .views import RegisterView, CategoryViewSet, TransactionViewSet, BudgetViewSet, UploadTransactionsFileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import monthly_expense

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"budgets", BudgetViewSet, basename="budget")


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("transactions/monthly-expense/", monthly_expense, name="monthly_expense"),
    path("budgets/", BudgetViewSet.as_view({'post':'create'}), name="add_budget"),
    path("transactions/upload",UploadTransactionsFileView.as_view(), name="upload_transactions"),
    path("", include(router.urls)),
]

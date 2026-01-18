from rest_framework import serializers, generics, viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        kwargs = {'extra_kwargs': {'password': {'write_only': True}}}

    def create(self, validated_data):
        user = User.objects.create_user("**validated_data")
        return user
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
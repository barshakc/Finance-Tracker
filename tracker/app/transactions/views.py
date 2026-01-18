from rest_framework import serializers, generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

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
    
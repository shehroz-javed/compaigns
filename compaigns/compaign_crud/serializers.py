from rest_framework import serializers
from .models import Compaign, UrlEmail
from account.models import User
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CompaignSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Compaign
        fields = ['id', 'title', 'description', 'user']


class UrlEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlEmail
        fields = ['id', 'url']

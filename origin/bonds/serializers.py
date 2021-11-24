from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth import get_user_model
from .models import Bond

user_model = get_user_model()


class BondSerializer(ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'
# Django Rest Framework
from rest_framework import serializers

# App
from django_package_boilerplate.models import ModelName


# Classes
class ModelNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelName
        fields = ['title', 'created_at', 'updated_at']

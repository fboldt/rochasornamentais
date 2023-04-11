from rest_framework import serializers
import app.models


class QuerySeralizer(serializers.ModelSerializer):
    class Meta:
        model = app.models.Query
        fields = '__all__'

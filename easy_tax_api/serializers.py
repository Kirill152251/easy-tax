from rest_framework import serializers


class DetailSerializer(serializers.Serializer):
    details = serializers.CharField()

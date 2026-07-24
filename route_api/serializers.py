from rest_framework import serializers


class RouteSerializer(serializers.Serializer):

    start = serializers.CharField(max_length=200)

    destination = serializers.CharField(max_length=200)
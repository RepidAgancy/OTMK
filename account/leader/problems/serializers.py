from rest_framework import serializers

from account import models


class LeaderProblemsSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(method_name='get_date')
    time = serializers.SerializerMethodField(method_name='get_time')

    class Meta:
        model = models.Problem
        fields = [
            'id', 'employee', 'date', 'time', 'comment', 'image'
        ]

    def get_date(self, obj):
        return obj.created_at.date()

    def get_time(self, obj):
        return obj.created_at.time()

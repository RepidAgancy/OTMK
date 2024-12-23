from rest_framework import serializers

from account import models


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = models.User
        fields = [
            'id', 'full_name', 'phone_number', 'profile_image',
        ]

    def get_full_name(self, obj):
        return obj.full_name


class LeaderProblemsSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(method_name='get_date')
    time = serializers.SerializerMethodField(method_name='get_time')
    employee = serializers.SerializerMethodField(method_name='get_employee')

    class Meta:
        model = models.Problem
        fields = [
            'id', 'employee', 'date', 'time', 'comment', 'image'
        ]

    def get_date(self, obj):
        return obj.created_at.date()

    def get_time(self, obj):
        return obj.created_at.time()

    def get_employee(self, obj):
        return EmployeeSerializer(obj.employee).data if obj.employee else None
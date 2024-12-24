from rest_framework import serializers

from account import models


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = models.User
        fields = [
            'id', 'full_name', 'phone_number', 'profile_image'
        ]

    def get_full_name(self, obj):
        return obj.full_name


class ProblemsSerializer(serializers.ModelSerializer):
    programmer = serializers.SerializerMethodField(method_name='get_programmer')
    date = serializers.SerializerMethodField(method_name='get_date')
    time = serializers.SerializerMethodField(method_name='get_time')

    class Meta:
        model = models.Problem
        fields = [
            'id', 'programmer', 'date', 'time', 'comment', 'image'
        ]

    def get_programmer(self, obj):
        return EmployeeSerializer(obj.employee).data

    def get_date(self, obj):
        return obj.created_at.date()

    def get_time(self, obj):
        return obj.created_at.time()


class KeepBusySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeepBusy
        fields = ['comment', 'image']



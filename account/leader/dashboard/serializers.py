from rest_framework import serializers

from account import models


class DashboardGetDateSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False, help_text='year-month-date')
    end_date = serializers.DateField(required=False, help_text='year-month-date')

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError("Cannot have a child older than start date end date ")
        return data


class ProgrammerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = models.User
        fields = ['id', 'full_name', 'phone_number', 'status']

    def get_full_name(self, obj):
        return obj.full_name


class ProblemsSerializer(serializers.ModelSerializer):
    programmer = serializers.SerializerMethodField(method_name='get_programmer')

    class Meta:
        model = models.Problem
        fields = ['id', 'programmer', 'problem_solve_time', 'comment', 'image']

    def get_programmer(self, obj):
        return ProgrammerSerializer(obj.programmer).data if obj.programmer else None
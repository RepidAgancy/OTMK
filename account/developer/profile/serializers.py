from rest_framework import serializers

from account import models


class ProfileGetDateSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False, help_text='year-month-date')
    end_date = serializers.DateField(required=False, help_text='year-month-date')

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError("Cannot have a child older than start date end date ")
        return data


class ProfileSolveProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ['id', 'comment', 'image', 'solve_date', 'start_time', 'end_time']


class ProfileKeepBusySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(method_name='get_date')

    class Meta:
        model = models.KeepBusy
        fields = [
            'id', 'start_time', 'end_time', 'comment', 'date'
        ]

    def get_date(self, obj):
        return obj.created_at.date()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = (
            {"phone_number": {"required": False}}
        )

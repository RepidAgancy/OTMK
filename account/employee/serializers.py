from rest_framework import serializers

from account import models


class GetDateSerializer(serializers.Serializer):
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
        fields = ("id", 'full_name', 'phone_number')

    def get_full_name(self, obj):
        return obj.full_name


class MyProblemsSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(source='get_date')
    programmer = serializers.SerializerMethodField(method_name='get_programmer')

    class Meta:
        model = models.Problem
        fields = (
            'id', 'status', 'comment', 'image', 'date', 'programmer'
        )

    def get_date(self, obj):
        return obj.created_at.date()

    def get_programmer(self, obj):
        programmer = obj.programmer
        return ProgrammerSerializer(programmer).data if obj.programmer else None


class SendProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = (
            'comment', 'image'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        problem = models.Problem.objects.create(
            comment=validated_data['comment'],
            employee=user,
        )
        problem.image = validated_data['image'] if validated_data.get('image') else None
        return problem

     


from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from account import models


class ProgrammerGetDateSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False, help_text='year-month-date')
    end_date = serializers.DateField(required=False, help_text='year-month-date')

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError("Cannot have a child older than start date end date ")
        return data


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ['id', 'problem_solve_time', 'comment', 'image']


class ProgrammersSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    problem = serializers.SerializerMethodField(method_name='get_problem')

    class Meta:
        model = models.User
        fields = ['id', 'full_name', 'phone_number', 'status', 'problem', 'profile_image']

    def get_problem(self, obj):
        problem = models.Problem.objects.filter(programmer__id=obj.id).last()
        return ProblemSerializer(problem).data if problem else None

    def get_full_name(self, obj):
        return obj.full_name


class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ['id', 'comment', 'image', 'solve_date', 'start_time', 'end_time']


class KeepBusiesSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(method_name='get_date')

    class Meta:
        model = models.KeepBusy
        fields = [
            'id',
            'start_time',
            'end_time',
            'comment',
            'image',
            'date'
        ]

    def get_date(self, obj):
        return obj.created_at.date()


class DeveloperAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'phone_number', 'password', 'profile_image']

    def create(self, validated_data):
        user = models.User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            password=make_password(validated_data['password']),
            role=models.PROGRAMMER,
            status=models.NOT_BUSY,
        )
        user.profile_image = validated_data['profile_image'] if validated_data['profile_image'] else None
        user.save()
        return user
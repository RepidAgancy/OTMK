from rest_framework import serializers

from account import models


class DeveloperSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = models.User
        fields = ['id', 'full_name', 'phone_number', 'profile_image']

    def get_full_name(self, obj):
        return obj.full_name


class TasksSerializer(serializers.ModelSerializer):
    programmers = serializers.SerializerMethodField(method_name='get_programmers')

    class Meta:
        model = models.Task
        fields = ['id', 'name', 'start_date', 'end_date', 'comment', 'programmers']

    def get_programmers(self, obj):
        return DeveloperSerializer(obj.programmers, many=True).data


class BoardSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(method_name='get_tasks')

    class Meta:
        model = models.Board
        fields = ['id', 'name', 'tasks']

    def get_tasks(self, obj):
        return TasksSerializer(obj.tasks, many=True).data
from rest_framework import serializers

from account import models


class CreateNewBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = [
            'name'
        ]


class TaskSerializer(serializers.ModelSerializer):
    programmers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects.filter(role=models.PROGRAMMER)
    )

    class Meta:
        model = models.Task
        fields = [
            'name', 'board', 'start_date', 'end_date', 'programmers', 'comment'
        ]


class ProgrammersListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = models.User
        fields = ['id', 'full_name', 'phone_number', 'profile_image']

    def get_full_name(self, obj):
        return obj.full_name


class GetTaskSerializer(serializers.ModelSerializer):
    programmers = serializers.SerializerMethodField(method_name='get_programmers')

    class Meta:
        model = models.Task
        fields = [
            'name', 'board', 'start_date', 'end_date', 'programmers', 'comment'
        ]

    def get_programmers(self, obj):
        return ProgrammersListSerializer(obj.programmers, many=True).data


class BoardSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(method_name='get_tasks')

    class Meta:
        model = models.Board
        fields = ['id', 'name', 'tasks']

    def get_tasks(self, obj):
        tasks = models.Task.objects.filter(board=obj)
        return GetTaskSerializer(tasks, many=True).data


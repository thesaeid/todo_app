from rest_framework import serializers
from .models import Task, Profile


class TaskSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "status",
            "created",
            "updated",
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "status",
            "created",
            "updated",
        )

    def create(self, validated_data):
        user_pk = self.context["user_pk"]
        profile, created = Profile.objects.get_or_create(user_id=user_pk)
        instance = Task.objects.create(profile=profile, **validated_data)
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "bio",
            "birth_date",
            "tasks",
        )


class ProfileCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "bio",
            "birth_date",
        )

    def create(self, validated_data):
        user = self.context["user"]
        instance = Profile.objects.create(user=user, **validated_data)
        return instance

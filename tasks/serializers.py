from rest_framework import serializers
from .models import Task, Profile


class TaskSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            # "location",
            "start_time",
            "end_time",
            "created",
            "updated",
            "notify",
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "notify",
            # "location",
            "start_time",
            "end_time",
            "created",
            "updated",
        )

    def create(self, validated_data):
        user_pk = self.context["user_pk"]
        profile = Profile.objects.get(user_id=user_pk)
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
        Profile.objects.filter(user=user).update(**validated_data)
        instance = Profile.objects.select_related("user").filter(user=user)
        return instance

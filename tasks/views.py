from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Task, Profile
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    ProfileSerializer,
    ProfileCreateSerializer,
)


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ("get", "put", "post", "delete")

    def get_queryset(self):
        return Task.objects.select_related("profile").filter(
            profile_id=self.kwargs["profile_pk"]
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskSerializer

    def get_serializer_context(self):
        return {"user_pk": self.request.user.id}


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ("get", "put", "delete")

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(
            user_id=self.request.user.id
        )

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return ProfileCreateSerializer
        return ProfileSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

from rest_framework.viewsets import ModelViewSet
from .models import Task, Profile
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    ProfileSerializer,
    ProfileCreateSerializer,
)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskSerializer

    def get_serializer_context(self):
        return {"user_pk": self.request.user.id}


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related("user").all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProfileCreateSerializer
        return ProfileSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

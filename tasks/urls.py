from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("profile", views.ProfileViewSet, basename="profile")

profile_router = routers.NestedDefaultRouter(
    router,
    "profile",
    lookup="profile",
)
profile_router.register(
    "tasks",
    views.TaskViewSet,
    basename="profile-tasks",
)

urlpatterns = router.urls + profile_router.urls

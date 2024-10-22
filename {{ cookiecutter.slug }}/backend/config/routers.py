from apps.users.views import UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("users", UserViewSet)

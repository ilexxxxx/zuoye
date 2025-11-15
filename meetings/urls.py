from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    MeetingViewSet, NotificationViewSet, register, RoomViewSet,
    check_conflict, UserListView, current_user
)

router = DefaultRouter()
router.register(r'meetings', MeetingViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),               # CRUD 路由
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', register),
    path('check-conflict/', check_conflict),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', current_user, name='current-user'),
]
from django.urls import path
from .views import UserCreate, UserList, UserDelete, UserDetail, PasswordResetCreate, PasswordResetConfirm


urlpatterns = [
    # User URLs
    path('users/', UserList.as_view(), name='user-list'),
    path('users/create/', UserCreate.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<int:pk>/delete/', UserDelete.as_view(), name='user-delete'),

    # Password Reset URLs
    path('password-reset/', PasswordResetCreate.as_view(), name='password-reset-create'),
    path('password-reset/confirm/<str:token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
]

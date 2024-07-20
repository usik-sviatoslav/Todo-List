from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.user.models import User
from apps.user.permissions import IsOwnerOrAdmin

from .filters import TodoFilter
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    serializer_class = TodoSerializer
    filterset_class = TodoFilter
    related_model = User
    model = Todo

    def get_queryset(self):
        queryset = self.model.objects.order_by("due_date")
        return queryset.filter(user_id=self.kwargs.get("user_id"))

    def get_object(self):
        return get_object_or_404(self.model, user_id=self.kwargs.get("user_id"), id=self.kwargs.get("pk"))

    def perform_create(self, serializer):
        serializer.save(user=get_object_or_404(self.related_model, id=self.kwargs.get("user_id")))

from django.urls import path
from drf_spectacular.utils import extend_schema

from .views import TodoViewSet

list_view = {"get": "list", "post": "create"}
detail_view = {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}

TodoViewSet = extend_schema(tags=["Todo"])(TodoViewSet)

urlpatterns = [
    path("", TodoViewSet.as_view(list_view), name="todo-list"),
    path("<int:pk>/", TodoViewSet.as_view(detail_view), name="todo-detail"),
]

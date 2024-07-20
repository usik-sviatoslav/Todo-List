from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Todo


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, attrs):
        due_date = attrs.get("due_date")
        current_time = timezone.localtime(timezone.now())

        if due_date and due_date <= current_time:
            raise ValidationError({"due_date": "Due date must be greater than current date."})

        return attrs

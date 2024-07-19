from django_filters import BooleanFilter, FilterSet, IsoDateTimeFilter

from .models import Todo


class TodoFilter(FilterSet):
    class Meta:
        model = Todo
        fields = ["due_date", "due_date__gte", "due_date__lte", "completed"]

    help_text = "Filter by the exact due date and time"
    due_date = IsoDateTimeFilter(field_name="due_date", lookup_expr="exact", help_text=help_text)

    help_text = "Filter by due date and time greater than or equal to the specified value"
    due_date__gte = IsoDateTimeFilter(field_name="due_date", lookup_expr="gte", help_text=help_text)

    help_text = "Filter by due date and time less than or equal to the specified value"
    due_date__lte = IsoDateTimeFilter(field_name="due_date", lookup_expr="lte", help_text=help_text)

    help_text = "Filter by completion status of the todo item"
    completed = BooleanFilter(field_name="completed", help_text=help_text)

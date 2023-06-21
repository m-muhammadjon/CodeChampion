import django_filters

from apps.problems.models import Attempt


class AttemptFilter(django_filters.FilterSet):
    mine = django_filters.BooleanFilter(method="filter_mine")

    class Meta:
        model = Attempt
        fields = [
            "mine",
        ]

    def filter_mine(self, queryset, name, value):
        if value:
            return queryset.filter(user=self.request.user)
        return queryset

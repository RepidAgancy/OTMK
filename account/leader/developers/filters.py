from django.db.models import Max, Min
from django_filters import rest_framework as filters

from account import models


class ProgrammerProblemFilterByProblemSolveTimeFilter(filters.FilterSet):
    FILTER_CHOICES = (
        ('least to most', 'Least to Most'),
        ('most to least', 'Most to Least'),
    )
    filter = filters.ChoiceFilter(choices=FILTER_CHOICES, method='filter_by_problem_solve_time')
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='gte', label="Start Date")
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='lte', label="End Date")

    class Meta:
        model = models.User
        fields = ['filter', 'start_date', 'end_date']

    def filter_by_problem_solve_time(self, queryset, name, value):
        queryset = queryset.annotate(
            max_solve_time=Max('problems_programmer__problem_solve_time'),
            min_solve_time=Min('problems_programmer__problem_solve_time')
        )

        if value == 'least to most':
            return queryset.order_by('min_solve_time')
        elif value == 'most to least':
            return queryset.order_by('-max_solve_time')
        return queryset

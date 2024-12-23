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
        if value == 'least to most':
            return queryset.order_by('problems_programmer__problem_solve_time').distinct()
        elif value == 'most to least':
            return queryset.order_by('-problems_programmer__problem_solve_time').distinct()
        return queryset.distinct()


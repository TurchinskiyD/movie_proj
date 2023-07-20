from django.contrib import admin, messages
from .models import Movie
from django.db.models import QuerySet

class RatingFilter(admin.SimpleListFilter):
    title = 'Фільтр по рейтингу'
    parameter_name = 'rating'
    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низький'),
            ('від 40 до 59', 'Середній'),
            ('від 60 до 79', 'Високий'),
            ('>=80', 'Найвищий'),
        ]
    def queryset(self, request, queryset:QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'від 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value() == 'від 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        if self.value() == '>=80':
            return queryset.filter(rating__gte=80)
        return queryset


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # fields = ['rating', 'name']
    # exclude = ['slug']
    # readonly_fields = ['slug']
    list_display = ['name', 'rating', 'currency', 'budget', 'rating_status']
    list_editable = ['rating', 'currency', 'budget']
    ordering = ['-rating', '-name']
    list_per_page = 10
    actions = ['set_dollars', 'set_euro']
    search_fields = ['name', 'rating']
    list_filter = ['name', 'currency', RatingFilter]

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Навіщо таке дивитися'
        if mov.rating < 70:
            return 'Один раз можна й глянути'
        if mov.rating <= 85:
            return 'Годиться'
        return 'Топчик'

    @admin.action(description='Встановити валюту в Долар')
    def set_dollars(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Встановити валюту в Євро')
    def set_euro(self, request, qs: QuerySet):
        count_update = qs.update(currency=Movie.EUR)
        self.message_user(
            request,
            f'Було оновлено {count_update} записи',
            messages.ERROR
        )

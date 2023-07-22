from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()
    slug = models.SlugField(blank=True, null=True)

    def get_url(self):
        return reverse('director-detail', args=[self.slug])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Actor(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDERS = [
        (MALE, "Чоловік"),
        (FEMALE, "Жінка")
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)

    def __str__(self):
        if self.gender == self.MALE:

            return f'Актор {self.first_name} {self.last_name}'
        else:
            return f'Актриса {self.first_name} {self.last_name}'


class Movie(models.Model):
    EUR = "EUR"
    USD = "USD"
    UAH = "UAH"
    CURRENCY_CHOICES = [
        (EUR, "Euro"),
        (USD, "Dollar"),
        (UAH, "Hryvnia")
    ]

    name = models.CharField(max_length=40)
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                 MaxValueValidator(100)])
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000,
                                 validators=[MinValueValidator(1)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=UAH)
    slug = models.SlugField(default='', null=False)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='movies')
    actors = models.ManyToManyField(Actor)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(args, kwargs)

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} - {self.rating}%'

# .\manage.py shell_plus --print-sql
# from movie_app.models import Movie


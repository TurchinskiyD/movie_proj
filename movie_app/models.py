from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

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
    director = models.CharField(max_length=100, default="Квентін Тарантіно")
    director_email = models.EmailField(default='director_email@gmail.com')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(args, kwargs)

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} - {self.rating}%'

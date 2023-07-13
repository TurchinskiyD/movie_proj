from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.db.models import F, Sum, Max, Min, Count, Avg, Value


# Create your views here.

def show_all_movie(request):
    movies = Movie.objects.order_by('rating', '-budget')  # name -name  id -id  budget і тд.
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
        str_field=Value('Hello'),
        number_field=Value(123),
        new_budget=F('budget')+80000,
        new_rating = F('rating')-2

    )
    # movies = Movie.objects.order_by(F('year').asc(nulls_last=True), '-rating')
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))

    # for mov in movies:
    #     mov.save()
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg
    })


def show_one_movie(request, slug_movie: str):
    # movie = Movie.objects.get(id=id_movie)
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html',
                  {'movie': movie})

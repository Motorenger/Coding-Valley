from django.http import Http404


def validate_imdb_rating(rating):
    if rating:
        try:
            float(rating)
        except ValueError:
            raise Http404
    return rating

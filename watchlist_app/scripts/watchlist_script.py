from django.db import connection
from watchlist_app.models import Review
from pprint import pprint


def run():
    review_queryset = Review.objects.all()
    pprint(review_queryset)
    pprint(connection.queries)

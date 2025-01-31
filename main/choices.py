from django.db import models


class BookTagChoices(models.TextChoices):
    FICTION = 'Fiction'
    FANTASY = 'Fantasy'
    COMEDY = 'Comedy'
    ADVENTURE = 'Adventure'
    ROMANCE = 'Romance'
    SCIFI = 'Sci-Fi'
    HISTORY = 'History'
    SELF_IMPROVEMENT = 'Self Improvement'

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.db import connection


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def create_choice_movies():
    from djan.models import movie_all, choice

    table_exists = 'djan_choice' in connection.introspection.table_names()

    if table_exists: 
        for movie in movie_all.objects.all():
            if not choice.objects.filter(movie=movie).exists():
                for i in range(1, 6):
                        choice.objects.create(movie=movie, choice_text=str(i), votes=0)


if __name__ == '__main__':
    main()
    create_choice_movies()

"""_summary_

    Returns:
        _type_: _description_
"""
from django.http import HttpResponse


def index(request): # type: ignore
    return HttpResponse("Hello, world. You're at the polls index.")
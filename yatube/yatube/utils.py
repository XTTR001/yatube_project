from django.conf import settings
from django.core.paginator import Page, Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest


def truncatechars(
    chars: str, max_length: int = settings.SHOWTEXT_LENGTH,
) -> str:
    return chars[:max_length] + '…' if len(chars) > max_length else chars


def get_page_obj(
        request: HttpRequest,
        queryset: QuerySet,
        pagesize: int = settings.PAGE_SIZE,
) -> Page:
    return Paginator(queryset, pagesize).get_page(request.GET.get('page'))

from django.conf import settings
from django.core.paginator import Paginator, Page
from django.http import HttpRequest


def truncatechars(
    chars: str, max_length: int = settings.SHOWTEXT_LENGTH
) -> str:
    return chars[:max_length] + '…' if len(chars) > max_length else chars


def get_page_obj(request: HttpRequest, objects) -> Page:
    paginator = Paginator(objects, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

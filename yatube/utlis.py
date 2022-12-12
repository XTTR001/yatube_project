from django.conf import settings


def truncatechars(chars: str) -> str:
    return (
        chars[: settings.SHOWTEXT_LENGTH] + '…'
        if len(chars) > settings.SHOWTEXT_LENGTH
        else chars
    )

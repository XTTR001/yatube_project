def truncatechars(chars: str, max_lenght) -> str:
    return (
        chars[: max_lenght] + '…'
        if len(chars) > max_lenght
        else chars
    )

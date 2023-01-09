import os
import sys


def main() -> None:
    """Запуск административных задач.

    Исключения:
        ImportError: если не получилось найти Django.
            Попробуйте активировать venv или установите: pip install django
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не получилось импортировать Django. Вы уверены, что Django "
            'установлен и доступен в PYTHONPATH перменной среды? Может быть '
            'вы забыли активировать виртуальное окружение?',
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

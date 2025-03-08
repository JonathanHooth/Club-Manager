from app.settings import DJANGO_ENABLE_CELERY


def delay_task(cb: callable, *args, **kwargs):
    """If celery is enabled schedule the task, or run immediately."""

    if DJANGO_ENABLE_CELERY:
        callable.delay(*args, **kwargs)
    else:
        callable(*args, **kwargs)

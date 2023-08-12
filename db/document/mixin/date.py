from mongoengine import DateTimeField, signals
from datetime import datetime


def trunc_millisecond(dt: datetime):
    return dt.replace(microsecond=dt.microsecond - (dt.microsecond % 1000))


def utcnow():
    now = datetime.utcnow()
    return trunc_millisecond(now)


def update_updated_at(sender, document):
    document.updated_at = utcnow()


class CreatedAtMixin:
    created_at = DateTimeField(default=utcnow)
    meta = {"abstract": True}


class UpdatedAtMixin:
    updated_at = DateTimeField(default=utcnow)
    meta = {"abstract": True}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        signals.pre_save.connect(update_updated_at, sender=cls)

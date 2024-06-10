import logging
import os


class classproperty:  # NOQA: E302
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class Loggable:
    """
    Use this mixin to do logging:
      self.logger.debug("My debugging message")
    """

    __logger = None

    @classproperty
    def logger(cls) -> logging.Logger:  # NOQA
        if cls.__logger:
            return cls.__logger

        cls.__logger = logging.getLogger(f"{cls.__module__}.{cls.__name__}")

        return cls.logger


class TestFilter(logging.Filter):
    def filter(self, record):  # pragma: no cover
        return not os.getenv("TEST_IS_RUNNING")

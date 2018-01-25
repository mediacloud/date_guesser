from enum import IntEnum

LOCALE = 'en'


class Accuracy(IntEnum):
    """Mark how accurate a publishing date guess is"""
    NONE = 0  # No guess at all
    PARTIAL = 1  # Some data gathered, might be missing a day
    DATE = 2  # Has ~date level accuracy, might be +/- 1 day
    DATETIME = 3  # Has datetime level accuracy, ~1ms


NO_METHOD = 'Did not find anything'


class Guess(object):
    """Date guessing result for the provided URL and its HTML contents."""

    __slots__ = [
        '__date',
        '__accuracy',
        '__method',
    ]

    def __init__(self, date, accuracy, method):
        self.__date = date
        self.__accuracy = accuracy
        self.__method = method

    @property
    def accuracy(self):
        """Accuracy of the guess."""
        return self.__accuracy

    @property
    def date(self):
        """datetime.datetime object with the guessed date, or None if a guess can't be made."""
        return self.__date

    @property
    def method(self):
        """Method that was used for guessing the date, or None if a guess can't be made."""
        return self.__method

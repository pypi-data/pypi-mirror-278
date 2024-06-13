# Standard Library Imports
from dataclasses import dataclass


@dataclass
class MessageException(Exception):
    message: str

    def __str__(self):
        return self.message


@dataclass
class ThrottlerException(Exception):
    pass


class QueueFullException(ThrottlerException, MessageException):
    message = "Queue is full. Please try again later"

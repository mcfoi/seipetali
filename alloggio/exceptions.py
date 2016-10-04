__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AlloggioUnavailable(Exception):
    pass

class AlloggioInvalidTimeslot(Exception):
    pass

class AlloggioNotActive(Exception):
    pass
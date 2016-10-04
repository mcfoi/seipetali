__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from reservation.models import Reservation
from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from user.models import User

class SessionStore(DbSessionStore):

    def cycle_key(self):

        super(SessionStore,self).cycle_key()

        # reservation_id = self.get('reservation_id',None)
        # if reservation_id:
        #     reservation = Reservation.objects.get(pk=reservation_id)
        #     uid = self.get('_auth_user_id')
        #     user = User.objects.get(id=uid)
        #
        #     reservation.user = user
        #     reservation.save()
        #
        # print 'SeipetaliSessionStore cycle_key', reservation_id


# At bottom to avoid circular import
from django.contrib.sessions.models import Session
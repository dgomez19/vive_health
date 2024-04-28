import datetime
import time

from .serializers import UserListRetrieveSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    date_time = datetime.datetime.now() + datetime.timedelta(hours=12)
    time_tuple = date_time.timetuple()
    exp = round(time.mktime(time_tuple) * 1000)
    return {
        'token': token,
        'user': UserListRetrieveSerializer(user, context={'request': request}).data,
        'exp': exp
    }

import os
import uuid
import secrets
import datetime

def applicationID():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    return timestamp + str(uuid.uuid4().int)[:10]
import uuid

def linkid():
    link = uuid.uuid4().hex[:8]
    return link
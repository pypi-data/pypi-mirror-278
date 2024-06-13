import json

from datetime import datetime
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)
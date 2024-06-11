import json
from _datetime import datetime
from pydantic import BaseModel



class Metadata(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None
    created_by: str = None
    updated_by: str = None


    def updateby(self, by: str):
        self.updated_by = by
        self.updated_at = datetime.now()

    def toDict(self):
        kv = {}
        if self.updated_by is not None:
            kv['updated_by'] = self.updated_by
            kv['updated_at'] = self.updated_at

        kv['created_by'] = self.created_by
        kv['created_at'] = self.created_at
        return kv

    @staticmethod
    def fromDict(kv: dict):
        metadata = Metadata(**kv)
        return metadata

    def tostring(self):
        json_string = json.dumps(self.toDict());
        return json_string

class Model(BaseModel):
    metadata: Metadata = None

    def updatedby(self, by: str):
        if self.metadata is None:
            self.metadata = Metadata({"reated_by":by, "updated_by":by})
        else:
            self.metadata.updated_by = by
            self.metadata.updated_at = datetime.now()
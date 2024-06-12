from pymongo import MongoClient
from pymongo.errors import InvalidURI
from typing import Optional


class MongoDB:
    def __init__(self, mongoUrl, mongoName: Optional[str]):
        self.url = mongoUrl
        self.name = mongoName

        if self.url:
            try:
                self.mDb = MongoClient(self.url)
                if self.name:
                    self._mongo = self.mDb[self.name]
                else:
                    self._mongo = self.mDb["FileSharingBot"]
            except InvalidURI:
                pass

    @property
    def mongo(self):
        return self._mongo

    def collection(self, name: str):
        return self._mongo[name]

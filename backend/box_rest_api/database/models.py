from box_rest_api.database import db
from sqlalchemy.dialects.mysql import INTEGER

class RFID_Uri_Mapping(db.Model):
    __tablename__ = 'mappings'
    rfid = db.Column(db.String(80), primary_key=True)
    uri = db.Column(db.String(80))
    offset = db.Column(INTEGER(unsigned=True))

    def __init__(self, rfid, uri):
        self.rfid = rfid
        self.uri = uri
        self.offset = 0

    def __repr__(self):
        return '<RFID_Uri_Mapping %r>' % self.title
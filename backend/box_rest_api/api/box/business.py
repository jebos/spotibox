from box_rest_api.database import db
from box_rest_api.database.models import RFID_Uri_Mapping

def create_rfid_uri_mapping(data):
    rfid = data.get('rfid')
    uri = data.get('uri')

    mapping = RFID_Uri_Mapping(rfid, uri)
    mapping.offset = data.get('offset')

    if mapping.offset == None:
        mapping.offset = 0

    db.session.add(mapping)
    db.session.commit()


def update_rfid_uri_mapping(id, data):
    mapping = RFID_Uri_Mapping.query.filter(RFID_Uri_Mapping.id == id).one()
    mapping.uri = data.get('uri')
    mapping.offset = data.get('offset')

    if mapping.offset == None:
        mapping.offset = 0

    db.session.add(mapping)
    db.session.commit()


def delete_rfid_uri_mapping(id):
    mapping = RFID_Uri_Mapping.query.filter(RFID_Uri_Mapping.id == id).one()

    db.session.delete(mapping)
    db.session.commit()

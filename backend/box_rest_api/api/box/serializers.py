from flask_restplus import fields
from box_rest_api.api.restplus import api

uri_mapping = api.model('Uri Mapping', {
    'id': fields.String(required=True, description='ID'),
    'uri': fields.String(required=True, description='Example: "spotify:track:1301WleyT98MSxVHPZCA6M"'),
    'offset': fields.Integer(description='Optional. Indicates from where in the context playback should start. Only available when context_uri corresponds to an album or playlist object, or when the uris parameter is used.'),
})

rfid_uri_mapping = api.model('RFID Uri Mapping', {
    'rfid': fields.String(required=True, description='RFID, one RFID can be mapped to many Spotify URIs, if so one random URI is played'),
    'uri': fields.String(required=True, description='Example: "spotify:track:1301WleyT98MSxVHPZCA6M"'),
    'offset': fields.Integer(description='Optional. Indicates from where in the context playback should start. Only available when context_uri corresponds to an album or playlist object, or when the uris parameter is used.'),
})

update_rfid_uri_mapping = api.model('Update RFID Uri Mapping', {
    'id' : fields.String(required=True, description='Internal ID'),
    'rfid': fields.String(required=True, description='RFID, one RFID can be mapped to many Spotify URIs, if so one random URI is played'),
    'uri': fields.String(required=True, description='Example: "spotify:track:1301WleyT98MSxVHPZCA6M"'),
    'offset': fields.Integer(description='Optional. Indicates from where in the context playback should start. Only available when context_uri corresponds to an album or playlist object, or when the uris parameter is used.'),
})

pagination = api.model('page results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_rfid_uri_mappings = api.inherit('Page of rfid_uri_mappings', pagination, {
    'items': fields.List(fields.Nested(rfid_uri_mapping))
})
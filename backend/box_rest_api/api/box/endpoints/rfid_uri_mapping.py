import logging

import random

from flask import request
from flask_restplus import Resource
from box_rest_api.api.box.business import create_rfid_uri_mapping, update_rfid_uri_mapping, delete_rfid_uri_mapping
from box_rest_api.api.box.serializers import rfid_uri_mapping, page_of_rfid_uri_mappings, uri_mapping, update_rfid_uri_mapping
from box_rest_api.api.box.parsers import pagination_arguments
from box_rest_api.api.restplus import api
from box_rest_api.database.models import RFID_Uri_Mapping

log = logging.getLogger(__name__)

ns = api.namespace('box/mapping', description='RFID Mapping')

@ns.route('/')
class RFIDUriMappingCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_rfid_uri_mappings)
    def get(self):
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        return RFID_Uri_Mapping.query.paginate(page, per_page, error_out=False)

    @api.expect(rfid_uri_mapping)
    def post(self):
        create_rfid_uri_mapping(request.json)
        return None, 201

@ns.route('/<string:rfid>')
@api.response(404, 'RFID Mapping not found.')
class RFID_Uri_MappingItem(Resource):

    @api.marshal_with(uri_mapping)
    def get(self, rfid):
        result = RFID_Uri_Mapping.query.filter(RFID_Uri_Mapping.rfid == rfid).all()
        if len(result) == 1:
            return result[0]

        #todo, add some real shuffel here.
        return result[random.randint(0,len(result))]
        

    @api.expect(update_rfid_uri_mapping)
    @api.response(204, 'Entry successfully updated.')
    def put(self, id):
        data = request.json
        update_rfid_uri_mapping(id, data)
        return None, 204

    @api.response(204, 'Entry successfully deleted.')
    def delete(self, id):
        delete_rfid_uri_mapping(id)
        return None, 204


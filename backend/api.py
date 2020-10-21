#!/usr/bin/python3

from flask import Flask, render_template
from flask_restful import Resource, Api
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort
from flask_cors import CORS

from PictureDB import PictureDB

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
CORS(app)

# could be a heartbeat or local time service?
class HelloWorld(Resource):
    def get(self):
        return { 'hello': 'world' }

api.add_resource(HelloWorld, '/')

#
# backend design
# pretend the date/time/cksum string is a unique identifier
# use 2 files as a database, one that holds date/time/cksum and filename
# and another that has date/time/cksum and tags.
#

class Pictures(Resource):

    first_id = '0000:00:00'
    last_id = '9999:99:99'
    getall_pictures_args = {
        # TODO add validation of any prefix string of YYYY:MM:DD HH:MM:SS ?
        "range_start": fields.Str(missing=first_id),
        "range_end": fields.Str(missing=last_id),
        "page_starts_at": fields.Str(missing=first_id),
        "page_starts_after": fields.Str(missing=first_id),
        "page_ends_before": fields.Str(missing=last_id),
        "page_ends_at": fields.Str(missing=last_id),
        "page_size": fields.Int(missing=100),
        "filter_string": fields.Str(missing=""),
    }

    pdb = PictureDB()

    @use_kwargs(getall_pictures_args, location="query")
    def get(self, 
            range_start, 
            range_end, 
            page_starts_at, 
            page_starts_after, 
            page_ends_before, 
            page_ends_at, 
            page_size, 
            filter_string):

        # default case
        mode = 'page_starts_at'
        where = self.first_id
        if page_ends_at != self.last_id:
            mode = 'page_ends_at'
            where = page_ends_at
        elif page_ends_before != self.last_id:
            mode = 'page_ends_before'
            where = page_ends_before
        elif page_starts_after != self.first_id:
            mode = 'page_starts_after'
            where = page_starts_after
        elif page_starts_at != self.first_id:
            mode = 'page_starts_at'
            where = page_starts_at
        
        # at most one of page_start_at, after, ends_before, at
        # is specified
        return Pictures.pdb.get_a_page_of_filtered_pictures(
                range_start, 
                range_end, 
                mode,
                where,
                page_size, 
                filter_string)

    # Note: no ability to add pictutures from client

api.add_resource(Pictures, '/pictures')

# /picture route
class Picture(Resource):
        
    patch_picture_args = {
        "tags": fields.Str(required=True),
    }

    pdb = PictureDB()

    # update tags on a picture
    @use_kwargs(patch_picture_args, location="json")
    def patch(self, id, tags):
        # only the tags can be updated, so rewrite tags file
        Picture.pdb.patch_tags(id, tags)
        return { "msg": "updated" }

    # note: no ability to delete pictures from client

api.add_resource(Picture, '/pictures/<string:id>')

# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

# vim: ts=4 sw=4 expandtab

# -*- coding: utf-8 -*-

from flask import abort, jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal
from tour.extensions import auth

points = [
    {
        'id': 1,
        'name': u'Bacacheri',
        'category': u'Park',
        'public': False,
        'latitude': -25.3898122,
        'longitude': -49.2399535
    },
    {
        'id': 2,
        'name': u'Tiki Liki',
        'category': u'Restaurant',
        'public': False,
        'latitude': -25.459473,
        'longitude': -49.2996737
    }
]

point_fields = {
    'name':      fields.String,
    'category':  fields.String,
    'public':    fields.Boolean,
    'latitude':  fields.Fixed,
    'longitude': fields.Fixed
}

@auth.get_password
def get_password(username):
    if username == 'robson':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

class PointsListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No point name provided', location='json')
        self.reqparse.add_argument('category', type=str, required=True,
                                   help='No point category provided', location='json')
        super(PointsListAPI, self).__init__()

    def get(self):
        return {'points': [marshal(point, point_fields) for point in points]}

    def post(self):
        args = self.reqparse.parse_args()
        point = {
            'id': points[-1]['id'] + 1,
            'name': args['name'],
            'category': args['category'],
            'public': False,
            'latitude': args['latitude'],
            'longitude': args['longitude']
        }
        points.append(point)

        return {'point': marshal(point, point_fields)}, 201

class PointsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('category', type=str, location='json')
        self.reqparse.add_argument('public', type=bool, location='json')
        self.reqparse.add_argument('latitude', type=int, location='json')
        self.reqparse.add_argument('longitude', type=int, location='json')
        super(PointsAPI, self).__init__()

    def get(self, id):
        point = [point for point in points if point['id'] == id]
        if len(point) == 0:
            abort(404)

        return {'point': marshal(point[0], point_fields)}

    def put(self, id):
        point = [point for point in points if point['id'] == id]
        if len(point) == 0:
            abort(404)
        point = point[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v is not None:
                point[k] = v

        return {'point': marshal(point, point_fields)}

    def delete(self, id):
        point = [point for point in points if point['id'] == id]
        if len(point) == 0:
            abort(404)
        points.remove(point[0])

        return {'result': True}

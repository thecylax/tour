# -*- coding: utf-8 -*-

from flask import abort, jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal
from tour.database import db
from tour.extensions import auth
from tour.public.models import Point
from tour.user.models import User

#points = [
#    {
#        'id': 1,
#        'name': u'Bacacheri',
#        'category': u'Park',
#        'public': False,
#        'latitude': '-25.3898122',
#        'longitude': '-49.2399535'
#    },
#    {
#        'id': 2,
#        'name': u'Tiki Liki',
#       'category': u'Restaurant',
#      'public': False,
#        'latitude': '-25.459473',
#        'longitude': '-49.2996737'
#    }
#]

point_fields = {
    'name':      fields.String,
    'category':  fields.String,
    'public':    fields.Boolean,
    'latitude':  fields.String,
    'longitude': fields.String
}


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    return True

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
        self.reqparse.add_argument('public', type=bool, required=False, location='json')
        self.reqparse.add_argument('latitude', type=str, required=False, location='json')
        self.reqparse.add_argument('longitude', type=str, required=False, location='json')
        super(PointsListAPI, self).__init__()

    def get(self):
        query = Point.query.all()

        points = []
        for point in query:
            point = {
                'name': point.name,
                'category': point.category,
                'public': point.public,
                'latitude': point.latitude,
                'longitude': point.longitude
            }
            points.append(point)

        return {'points': [marshal(point, point_fields) for point in points]}

    def post(self):
        args = self.reqparse.parse_args()
        name = args['name'],
        category = args['category'],
        public = args['public'] if args['public'] is not None else False
        latitude = args['latitude'] if args['latitude'] is not None else '0'
        longitude = args['longitude'] if args['longitude'] is not None else '0'

        point = Point(name=name,
                      category=category,
                      public=public,
                      latitude=latitude,
                      longitude=longitude)

        db.session.add(point)
        db.session.commit()

        point = {
            'name': name[0],
            'category': category[0],
            'public': public,
            'latitude': latitude,
            'longitude': longitude
        }

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
        query = Point.query.filter_by(id=id).first()

        if query is not None:
            point = {
                'name': query.name,
                'category': query.category,
                'public': query.public,
                'latitude': query.latitude,
                'longitude': query.longitude
            }
        else:
            abort(404)

        return {'point': marshal(point, point_fields)}

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
        query = Point.query.filter_by(id=id).first()

        if query is not None:
            db.session.delete(query)
            db.session.commit()
        else:
            abort(404)

        return {'result': True}

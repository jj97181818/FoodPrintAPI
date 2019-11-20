from flask import jsonify
from flask_restful import Resource
from flask_login import login_required, current_user


class Information(Resource):
    @login_required
    def get(self):
        username = current_user.get_id()
        return jsonify({'data': 'You got the resource, {}'.format(username)})

from flask import request
from flask_restful import Resource, reqparse
from piolin.db import db
from piolin.models.message import Message
from piolin.routes.utils import verify_token, get_date

# define the MessageAPI resource
class MessageAPI(Resource):
    # get all messages for a user
    def get(self):
        user = verify_token(request)
        if not user:
            return {'message': 'Unauthorized'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('to', type=str, required=False)
        parser.add_argument('from', type=str, required=False)
        args = parser.parse_args()

        if args['to']:
            sender = user
            receiver = args['to']
        elif args['from']:
            receiver = user
            sender = args['from']
        else:
            return {'message': 'Missing to or from parameter'}, 400

        # get messages sent or received by user
        messages = Message.query.filter_by(receiver=receiver).filter_by(sender=sender).all()

        return [{'from': message.sender, 'to': message.receiver,
                 'text': message.body, 'date': message.date} for message in
                messages], 200

    # create a new message
    def post(self):
        user = verify_token(request)
        if not user:
            return {'message': 'Unauthorized'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('to', type=str, required=True)
        parser.add_argument('text', type=str, required=True)
        args = parser.parse_args()

        # create new message and add to database
        message = Message(sender=user, receiver=args['to'],
                          body=args['text'], date=get_date())
        db.session.add(message)
        db.session.commit()

        return {'message': 'Message sent successfully'}, 201

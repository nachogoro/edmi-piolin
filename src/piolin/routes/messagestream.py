from flask import request, Response, current_app, stream_with_context
from flask_restful import Resource, reqparse
from piolin.db import db
from piolin.models.message import Message
from piolin.routes.utils import verify_token, get_date
import time

# define the MessageStreamAPI resource
class MessageStreamAPI(Resource):
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

        print(current_app)
        def generate(receiver: str, sender: str):
            already_notified = set()

            while True:
                to_send = []

                messages = Message.query.filter_by(receiver=receiver).filter_by(sender=sender).all()

                for msg in messages:
                    if msg.id not in already_notified:
                        already_notified.add(msg.id)
                        yield f'{{"sender": "{msg.sender}", "receiver": "{msg.receiver}", "text": "{msg.body}", "date": "{msg.date}"}}\n'

                yield '{}\n'
                time.sleep(3)

        return Response(stream_with_context(generate(receiver, sender)), mimetype='application/x-ndjson')

from flask import request
from flask_restful import Resource, reqparse
from piolin.db import db
from piolin.models.tweet import Tweet
from piolin.models.user import User
from piolin.routes.utils import verify_token, get_date

class TweetAPI(Resource):
    # get all tweets for an author
    def get(self, nickname):
        tweets = Tweet.query.filter_by(author=nickname).all()
        return [{'id': tweet.id, 'author': tweet.author, 'text': tweet.text,
                 'date': tweet.date} for tweet in tweets]

    # create a new tweet for an author
    def post(self):
        user = verify_token(request)
        if not user:
            return {'message': 'Unauthorized'}, 401

        # parse request body for tweet text
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, required=True)
        args = parser.parse_args()

        # create new tweet and add to database
        tweet = Tweet(author=user, text=args['text'], date=get_date())
        db.session.add(tweet)
        db.session.commit()

        return {'message': 'Tweet created successfully', 'id': tweet.id}, 201

    def delete(self):
        user = verify_token(request)
        if not user:
            return {'message': 'Unauthorized'}, 401

        # parse request body for tweet text
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='args')
        args = parser.parse_args()

        tweet = Tweet.query.filter_by(id=args['id']).first()

        if not tweet:
            return {'error': 'Tweet not found'}, 404

        if tweet.author != user:
            return {'error': 'Unauthorised'}, 403

        # create new tweet and add to database
        db.session.delete(tweet)
        db.session.commit()

        return {}, 204

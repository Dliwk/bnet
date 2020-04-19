from app import api
from flask_restful import Resource, abort
from flask import jsonify
from apis import local
from exceptions import LocalApi


@api.resource('/chat/<int:chat_id>')
class ChatResource(Resource):
    def get(self, chat_id):
        chat = None
        try:
            chat = local.chats.get_chat(chat_id)
        except LocalApi.NotFoundError:
            abort(404, message='chat not found')
        return jsonify(chat, only=['id', 'title', 'users', 'messages'])

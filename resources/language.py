from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.language import LanguageModel


class Language(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('voice',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        language = LanguageModel.find_by_name(name)
        if language:
            return language.json()
        return {'message': 'Language not found'}, 404

    @jwt_required()
    def post(self, name):
        if LanguageModel.find_by_name(name):
            return {'message': "A language with name '{}' already exists.".format(name)}, 400

        data = Language.parser.parse_args()
        language = LanguageModel(name, **data)

        try:
            language.save_to_db()
        except:
            return {"message": "An error occurred creating the language."}, 500

        return language.json(), 201

    @jwt_required()
    def put(self, name):
        language = LanguageModel.find_by_name(name)
        if not language:
            return {'message': 'Language not found'}, 404

        data = Language.parser.parse_args()
        updated_language = LanguageModel(name, **data)
        language.voice = updated_language.voice

        try:
            language.save_to_db()
        except:
            return {"message": "An error occurred updating the language."}, 500

        return language.json(), 201

    @jwt_required()
    def delete(self, name):
        language = LanguageModel.find_by_name(name)
        if language:
            language.delete_from_db()

        return {'message': 'Language deleted'}


class LanguageList(Resource):
    def get(self):
        return {'languages': list(map(lambda x: x.json(), LanguageModel.query.all()))}

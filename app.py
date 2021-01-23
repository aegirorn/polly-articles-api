import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import datetime

from security import authenticate, identity
from resources.user import UserRegister
from resources.language import Language, LanguageList
from resources.article import Article, ArticleList

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)
app.secret_key = 'oursupersecretabracadabrahocuspocus'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Language, '/language/<string:name>')
api.add_resource(LanguageList, '/languages')
api.add_resource(Article, '/article/<string:title>')
api.add_resource(ArticleList, '/articles')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

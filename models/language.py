from db import db


class LanguageModel(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    voice = db.Column(db.String(80))

    articles = db.relationship('ArticleModel', lazy='dynamic')

    def __init__(self, name, voice):
        self.name = name
        self.voice = voice


    def json(self):
        return {'id': self.id, 'name': self.name, 'voice': self.voice, 'articles': [article.json() for article in self.articles.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
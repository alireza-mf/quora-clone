from datetime import datetime
from typing import List
from slugify import slugify

from db import db
from models.answer import AnswerModel


class QuestionModel(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    answers = db.relationship("AnswerModel", lazy="dynamic")
    user = db.relationship("UserModel", backref="question")

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)

    @classmethod
    def find_by_slug(cls, slug: str) -> "QuestionModel":
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_all(cls) -> List["QuestionModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ """
    __tablename__ = 'user'

    # table definition:
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    # create_at = db.Column(db.DateTime, server_default=func.now())
    # update_at = db.Column(db.DateTime, server_default=func.now(), 
    #                                    server_onupdate=db.func.now())


class IntentLabels(db.Model):
    """Intent level labels"""

    __tablename__ = 'intent_labels'

    intent_label_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intent_label = db.Column(db.String(50), nullable=False)
    # annotator_id = db.Column(db.Integer, ForeignKey="user.user_id")


class EntityLabels(db.Model):
    """Entity level labels"""

    __tablename__ = 'entity_labels'

    entity_label_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entity_label = db.Column(db.String(50))
    intent_label_id = db.Column(db.Integer, 
                                ForeignKey='intent_labels.intent_label_id')
    annotator_id = db.Column(db.Integer, ForeignKey="user.user_id")


class Entity():
    """Labeled entities that have been extracted from the sentence"""

    __tablename__ = 'entities'

    entity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entity = db.Column(db.String(50))
    line_id = db.Column(db.Integer, ForeignKey='')  # this may change to dataset_id depending on how we're storing our data


# helper functions below
def init_app():
    from flask import Flask
    app = Flask(__name__)
    db.init_app(app)
    return app


def connect_to_db(app, db_uri='postgresql://postgres:mideata666666@pg.mideata.com:5432/postgres'):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app()

if __name__ == "__main__":

    app = init_app(app)
    connect_to_db(app)

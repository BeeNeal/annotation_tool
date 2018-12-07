from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///template1'
db = SQLAlchemy(app)


class User(db.Model):
    """ """
    __tablename__ = 'users'

    # table definition:
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    # create_at = db.Column(db.DateTime, server_default=func.now())
    # update_at = db.Column(db.DateTime, server_default=func.now(), 
    #                                    server_onupdate=db.func.now())


class IntentLabel(db.Model):
    """Intent level labels"""

    __tablename__ = 'intent_labels'

    intent_label_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intent_label = db.Column(db.String(255), nullable=False, unique=True)
    # annotator_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    closed_set = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Intent Label label={self.intent_label} >"


class EntityLabel(db.Model):
    """Entity level labels- assumes there is an associated intent label"""

    __tablename__ = 'entity_labels'

    entity_label_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entity_label = db.Column(db.String(255))
    intent_label = db.Column(db.String(255), 
                                db.ForeignKey('intent_labels.intent_label'))
    closed_set = db.Column(db.Boolean, default=False)

    # intent_label_id = db.Column(db.Integer, 
    #                             db.ForeignKey('intent_labels.intent_label_id'))
    # annotator_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Entity Label label={self.entity_label} >"


class Entity():
    """Labeled entities that have been extracted from the sentence"""

    __tablename__ = 'entities'

    entity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entity = db.Column(db.String(255))
    entity_label = db.Column(db.String(255), 
                             db.ForeignKey('entity_labels.entity_label'))
    text_id = db.Column(db.Integer, db.ForeignKey('text.text_id'))  



# need some type of labeling 'instance' to connect annotator with label
# Wouldn't want to store the instance label on the annotator iteself, b/c it's an
# action of the annotator, not a characteristic


# helper functions below

# def connect_to_db(app, db_uri='postgresql:///annotool'):
#     """Connect the database to our Flask app."""

#     # Configure to use our database.
#     app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     db.app = app

# if __name__ == "__main__":

#     # midea_postgres = 'postgresql://postgres:mideata666666@pg.mideata.com:5432/postgres'
#     # add midea postgres to connect to db when ready
#     connect_to_db(app)
#     db.create_all()

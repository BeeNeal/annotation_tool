from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ """
    __tablename__ = 'user'

    # table definition:
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, server_default=func.now())
    update_at = db.Column(db.DateTime, server_default=func.now(), 
                                       server_onupdate=db.func.now())


class IntentLabels(db.Model):
    """Agreed upon intent level labels """

    __tablename__ = 'intent_labels'

    intent_label_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intent_label = db.Column(db.String(50), nullable=False)
    annotator_id = db.Column(db.Integer, ForeignKey="user.user_id")


class OpenLabels():
    """Intent level labels that may differ from annotator to annotator"""

     __tablename__ = 'closed_labels'

    op_label_id = Column(INTEGER, Sequence('op_label_id_seq'), primary_key=True)
    label = Column(VARCHAR(50))
    annotator_id = Column(INTEGER, ForeignKey="user.user_id")


class EntityLabeled():
    """Labeled entities that have been extracted from the sentence"""

    __tablename__ = 'entity_labeled'

    entity_id = Column(INTEGER, Sequence('entity_id_seq'), primary_key=True)
    file_id = Column(VARCHAR(255))  # links line to file it came from
    intent_label = Column(VARCHAR(50), ForeignKey='labels.label')
    entity = Column(VARCHAR(50))


if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
import os

import flask
import flask_sqlalchemy

app = flask.Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE"]
app.config["IMAGE_DIR"] = os.environ["IMAGE_DIR"]

db = flask_sqlalchemy.SQLAlchemy(app)

class CustomEncoder(flask.json.JSONEncoder):
    def default(self, obj):  # pylint: disable=W0237
        if isinstance(obj, db.Model):
            return obj.to_serializable()

        return super().default(obj)
app.json_encoder = CustomEncoder

import models  # pylint: disable=C0413,W0611
import handlers  # pylint: disable=C0413,W0611

def sync_to_upload_directory():
    models.Image.sync_table_to_directory(app.config["IMAGE_DIR"])

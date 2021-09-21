import os

from app import db


class Image(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    cell_width = db.Column(db.Integer())

    @classmethod
    def sync_table_to_directory(cls, path):
        all_image_ids = {i.id for i in cls.query.all()}
        missing_image_ids = set(os.listdir(path)) - all_image_ids
        for image_id in missing_image_ids:
            db.session.add(cls(id=image_id))
        db.session.commit()


    def to_serializable(self):
        return {
            "id": self.id,
            "cell_width": self.cell_width,
        }

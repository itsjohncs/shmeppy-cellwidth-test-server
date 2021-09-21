import flask

from app import app
from models import Image


@app.route("/images")
def list_images():
    return {
        "result": "success",
        "images": Image.query.all(),
    }


@app.route("/images/<image_id>/meta")
def get_image_metadata(image_id):
    image = Image.query.filter_by(id=image_id).first()
    if not image:
        return {
            "result": "error",
            "message": f"can't find image with ID {image_id}"
        }, 404
    else:
        return {
            "result": "success",
            "image": image,
        }


@app.route("/images/<image_id>/meta", methods=["POST"])
def update_image_metadata(image_id):
    cell_width = flask.request.json.get("cell_width")
    if not cell_width:
        return {
            "result": "error",
            "message": "cell_width is a required parameter",
        }, 400

    num_updated_rows = (
        Image.filter_by_(id=image_id).update({Image.cell_width: cell_width}))
    if num_updated_rows == 0:
        return {
            "result": "error",
            "message": f"could not find image with ID {image_id}"
        }, 404

    return {"result": "success"}


@app.route("/images/<image_id>", methods=["GET"])
def get_image(image_id):
    return flask.send_from_directory(app.config["IMAGE_DIR"], image_id)

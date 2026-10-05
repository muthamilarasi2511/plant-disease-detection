from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return render_template(
            "index.html",
            error="Please select an image."
        )

    file = request.files["image"]

    if file.filename == "":
        return render_template(
            "index.html",
            error="Please select an image."
        )

    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            error="Only JPG, JPEG, PNG and WEBP images are allowed."
        )

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Temporary demo result
    # Replace this with the trained AI model later.
    plant = "Tomato"
    disease = "Early Blight"
    confidence = "94%"

    return render_template(
        "index.html",
        prediction=True,
        plant=plant,
        disease=disease,
        confidence=confidence,
        filename=filename
    )


if __name__ == "__main__":
    app.run(debug=True)
import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    flash
)
from validator import Validator

UPLOAD_FOLDER = '/tmp/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(file_obj):
    return True
    # return filename.ends_with('.txt')

def validate_input_file(file_obj):


@app.route("/representation", methods=['POST'])
def representation():

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    uploaded_file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if uploaded_file and allowed_file(uploaded_file):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('representation.html')


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

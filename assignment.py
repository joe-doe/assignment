
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    flash
)
from validator import Validator
from reconstructure import Reconstruction

UPLOAD_FOLDER = '/tmp/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


@app.route("/representation", methods=['GET', 'POST'])
def representation():
    is_validation_pass, flash_message = Validator(request, request.files['file']).get_results()

    if not is_validation_pass:
        flash(flash_message)
        return render_template('index.html')
    return render_template('representation.html')

    # # check if the post request has the file part
    # if not validator.is_post_name_correct(request):
    #     flash('No file part')
    #     return redirect(request.url)
    #
    # uploaded_file = request.files['file']
    #
    # # if user does not select file, browser also
    # # submit a empty part without filename
    # if validator.is_empty_filename(uploaded_file):
    #     flash('No selected file')
    #     return redirect(request.url)
    #
    # if validator.is_tar(uploaded_file):
    #     filename = secure_filename(uploaded_file.filename)
    #     uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     return render_template('representation.html')


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/reconstruct", methods=['GET'])
def reconstruct():
    a = Reconstruction()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

import os
from urllib import response

from flask import Flask, flash, request, redirect, url_for, json, render_template
from werkzeug.utils import secure_filename
import base64
import requests

UPLOAD_FOLDER = "C:/Users/SESA646403/Documents/New folder/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": '92ceb1a1e051b4f44f25a645c6539fbb',
                    "image": base64.b64encode(file.read()),
                }
                res = requests.post(url, payload)
                response_dict = json.loads(res.text)
                url_of_photo = response_dict['data'].get('display_url')
                return render_template('/index.html', url_of_photo=url_of_photo)

    return render_template('/index.html')


if __name__ == '__main__':
    app.run()

import os
from flask import Flask, render_template, request , Response,send_file
from stt import *

__author__ = 'YY20'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'audio/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    mainSTT(destination)

    return send_file(os.path.join(APP_ROOT, 'csv/out.csv'),
                     mimetype='text/csv',
                     attachment_filename=filename.split('.')[0]+'.csv',
                     as_attachment=True)
 

if __name__ == "__main__":
    app.run(port=4555, debug=True)
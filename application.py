import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
 
UPLOAD_FOLDER = 'static/uploads'
 
application = Flask(__name__)
application.secret_key = "secret key"
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   
@application.route('/')
def upload_form():
    return render_template('upload.html')
 
@application.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        print(filename)
        flash('Image successfully uploaded and displayed below')
        os.system(f'python models/demo.py image -n models/yolox_s.py -c models/yolox_s.pth --path models/{filename} --conf 0.01 --nms 0.65 --tsize 640 --save_result --device cpu')
        print('After')
        return render_template('upload.html', filename='static/yolox_output/dogs.jpeg')
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
 
@application.route('/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", port="80")

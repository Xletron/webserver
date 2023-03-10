import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from urllib.parse import unquote

app = Flask(__name__)

HOME = 'X:/'

app.config['HOME'] = HOME

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'ico'}

def is_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    path = request.args.get('path', '')
    full_path = os.path.join(app.config['HOME'], unquote(path))
    if not os.path.exists(full_path):
        return 'Invalid path'

    files = []
    for filename in os.listdir(full_path):
        file_path = os.path.join(full_path, filename)
        if os.path.isdir(file_path):
            filename += '/'
            files.insert(0, {'name': filename, 'is_image': False})
        else:
            is_video = filename.endswith('.mp4')
            video_path = url_for('video', filename=unquote(path) + '/' + filename) if is_video else None
            files.append({'name': filename, 'is_image': is_image(filename), 'is_video': is_video, 'video_path': video_path})

    parent_dir = os.path.dirname(os.path.dirname(path))
    if not parent_dir:
        parent_dir = '/'
    else:
        parent_dir = unquote(parent_dir) + '/'
    
    header = "Index of " + full_path
    return render_template('index.html', files=files, path=path, parent_dir=parent_dir.rstrip('/'), unquote=unquote, header=header)


@app.route('/download/<path:filename>')
def download(filename):
    path = request.args.get('path', '')
    full_path = os.path.join(app.config['HOME'], unquote(path))
    file_path = os.path.join(full_path, filename)
    if not os.path.exists(file_path):
        return 'File not found'
    return send_file(file_path, as_attachment=True)

@app.route('/video/<path:filename>')
def video(filename):
    path = request.args.get('path', '')
    full_path = os.path.join(app.config['HOME'], unquote(path))
    file_path = os.path.join(full_path, filename)
    if not os.path.exists(file_path):
        return 'File not found'
    print(file_path)
    return send_file(file_path, mimetype='video/mp4')

@app.route('/thumbnail/<path:filename>')
def thumbnail(filename):
    path = request.args.get('path', '')
    full_path = os.path.join(app.config['HOME'], unquote(path))
    file_path = os.path.join(full_path, filename)
    return send_file(file_path, mimetype='image')

@app.route('/upload', methods=['POST'])
def upload():
    path = request.args.get('path', '')
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['HOME'], unquote(path))
        file.save(os.path.join(full_path, filename))
    return redirect(url_for('index', path=path))



def allowed_file(filename):
    return True


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

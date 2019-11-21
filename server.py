import os
from flask import Flask, render_template, send_from_directory, request, send_file
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/uploader/content', methods = ['GET', 'POST'])
def upload_file_content():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.root_path, 'static/content/') + secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/uploader/style', methods = ['GET', 'POST'])
def upload_file_style():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.root_path, 'static/style/') + secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/output/<filename>')
def output(filename):
    return send_file(os.path.join(app.root_path, 'static/output/') + filename + '.jpg', mimetype='image')

@app.route('/transfer', methods = ['GET', 'POST'])
def transfer():
    content_image = request.args.get('content')
    style_image = request.args.get('style')
    return 'http://127.0.0.1:5000/output/chicago_la_muse'

if __name__ == '__main__':
    app.run()

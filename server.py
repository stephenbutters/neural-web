import os
import sys
from flask import Flask, render_template, send_from_directory, request, send_file
from werkzeug import secure_filename
import transfer as tran
app = Flask(__name__)
address = sys.argv[1]

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
    content_image = os.path.join(app.root_path, 'static/content/') + request.args.get('content')
    style_image = os.path.join(app.root_path, 'static/style/') + request.args.get('style')
    num_iterations = int(request.args.get('num_iterations'))
    rate = float(request.args.get('rate'))
    option = request.args.get('option')
    if option not in {'face', 'else', 'all'}:
        return "Invalid Option"

    if not os.path.exists(content_image) or not os.path.exists(style_image):
        return "Image Not Exists"

    best_image, best_loss = tran.run(content_image, style_image, num_iterations, rate, option=option)

    content_image_prefix = request.args.get('content').split('.')[0]
    style_image_prefix = request.args.get('style').split('.')[0]
    output_image_name = content_image_prefix + '_' + style_image_prefix + '_' + option
    best_image.save(os.path.join(app.root_path, 'static/output/') + output_image_name + '.jpg')

    return 'http://{}/output/'.format(address) + output_image_name

if __name__ == '__main__':
    app.run()

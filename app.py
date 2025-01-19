from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageFilter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

# Проверка и создание директории для загрузки изображений
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('process_image', filename=file.filename))

@app.route('/process_image/<filename>')
def process_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with Image.open(filepath) as img:
        img.load()
        img = img.filter(ImageFilter.BLUR)
        img = img.rotate(180)
        processed_filename = f"processed_{filename}"
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        img.save(processed_filepath)
    return render_template('home.html', processed=processed_filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>')
def delete_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

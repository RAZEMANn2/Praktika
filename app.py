from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageFilter
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
db = SQLAlchemy(app)

# Проверка и создание директории для загрузки изображений
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)

@app.route('/')
def home():
    images = ImageModel.query.all()
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
        new_image = ImageModel(filename=file.filename)
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('process_image', filename=file.filename))

@app.route('/process_image/<filename>')
def process_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with Image.open(filepath) as img:
        img.load()
        img = img.rotate(90)
        img = img.filter(ImageFilter.BLUR)
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
    image = ImageModel.query.filter_by(filename=filename).first()
    if image:
        db.session.delete(image)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

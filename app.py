from flask import Flask, request, render_template, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Главная страница с формой для загрузки файлов
@app.route('/')
def index():
    return render_template('index.html')

# Обработка загрузки файлов
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    image_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_files.append(file_path)
    
    if image_files:
        pdf_path = create_pdf(image_files)
        return send_file(pdf_path, as_attachment=True)
    else:
        return redirect(url_for('index'))

# Функция для создания PDF из изображений
def create_pdf(image_files):
    pdf = FPDF()
    for image in image_files:
        pdf.add_page()
        pdf.image(image, x=10, y=10, w=pdf.w - 20)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.pdf')
    pdf.output(pdf_path)
    return pdf_path

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)

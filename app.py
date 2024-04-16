#   /Website
#       app.py
#       /templates
#               index.html
#       /static
#           /css
#               style.css
#           /image
#               logo.png
#       /uploads
#           csv generate output: DeepSP_descriptors.csv

from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, abort, send_file
import os
from urllib.parse import quote as url_quote

import csv

from main import process_file

app = Flask(__name__)

app.secret_key = 'pkl'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt','csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])

def home():
    csv_path = request.args.get('csv_path', None)
    #print("csv_path:", csv_path)  # This will print the value of csv_path to your console
    return render_template('index.html', csv_path=csv_path)

def write_to_csv(data, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Heavy_Chain', 'Light_Chain']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)
    return filepath


@app.route('/upload', methods=['POST'])

def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = url_quote(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    mab_data = {
        'Name': request.form['mab_name'],
        'Heavy_Chain': request.form['heavy_chain'],
        'Light_Chain': request.form['light_chain']
    }
    filepath = write_to_csv(mab_data, 'input_data.csv')

    try:
        # Assume process_file processes the CSV and returns path of generated CSV
        processed_csv_path = process_file(filepath)
        csv_filename = os.path.basename(processed_csv_path)
        return redirect(url_for('home', csv_path=csv_filename))
    except Exception as e:
        flash(f'Error processing file: {e}')
        return redirect(request.url)
    
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    directory = "uploads"
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
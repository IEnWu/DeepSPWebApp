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


@app.route('/upload', methods=['GET','POST'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')  # Using .get is safer for dict access
        if file and file.filename:
            if allowed_file(file.filename):
                filename = url_quote(file.filename)  # Use secure_filename to avoid security issues
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # If you need to do something with the file, add that logic here

        # Handle form data and write to CSV
        mab_data = {
            'Name': request.form.get('mab_name', ''),
            'Heavy_Chain': request.form.get('heavy_chain', ''),
            'Light_Chain': request.form.get('light_chain', '')
        }
        filepath = write_to_csv(mab_data, 'input_data.csv')
        try:
            processed_csv_path = process_file(filepath)  # This function should handle file processing
            csv_filename = os.path.basename(processed_csv_path)
            return redirect(url_for('home', csv_path=csv_filename))
        except Exception as e:
            flash(f'Error processing file: {e}')
            return redirect(url_for('upload_file'))  # Redirect to the same page to try again
    return render_template('index.html')  # Ensure you have a GET handler to display the form

    
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    directory = "uploads"
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
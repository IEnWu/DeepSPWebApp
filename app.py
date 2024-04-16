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

def write_to_csv(data):
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Heavy_Chain', 'Light_Chain']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)



@app.route('/upload', methods=['GET','POST'])
def upload_file():
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = url_quote(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            heavy_chain = request.form['heavy_chain']
            light_chain = request.form['light_chain']
            mab_name = request.form['mab_name']

            filepath = {'Name': mab_name, 'Heavy_Chain': heavy_chain, 'Light_Chain': light_chain}
            write_to_csv(filepath)

            process_file(filepath)
        # Process the file to generate CSV
            try:
                # Process the file
                full_csv_path = process_file(filepath)  # Assume process_file now returns path of generated CSV
                # Pass the CSV path or its data to the template
                csv_filename = os.path.basename(full_csv_path)
                return redirect(url_for('home', csv_path=csv_filename))
            except Exception as e:
                flash(f'Error processing file: {e}')
                return redirect(request.url)
                   
    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    directory = "uploads"
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
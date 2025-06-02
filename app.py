from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# CSV File Path
CSV_FILE = 'leads.csv'
CSV_HEADERS = ['Nombre', 'Email', 'Voluntario Organizador']

def initialize_csv():
    # Create CSV with headers if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        voluntario = 'Sí' if request.form.get('voluntario') else 'No'

        # Append data to CSV
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([nombre, email, voluntario])

        # For now, let's redirect to a simple success page or back to the form
        # We will create a proper success message/page in a later step
        return render_template('success.html')

if __name__ == '__main__':
    initialize_csv() # Ensure CSV is ready when app starts
    app.run(host='0.0.0.0', port=5000, debug=True)

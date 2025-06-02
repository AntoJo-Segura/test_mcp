from flask import Flask, jsonify
import csv
import os

app = Flask(__name__)

# Path to the CSV file - assuming it's in the parent directory
# In a containerized setup, this path might need to be adjusted or the file mounted.
LEADS_CSV_PATH = '/csv_data/leads.csv'

def read_leads():
    """Reads data from the leads.csv file."""
    leads = []
    if not os.path.exists(LEADS_CSV_PATH):
        return leads # Return empty list if CSV not found

    try:
        with open(LEADS_CSV_PATH, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}") # Log error
        return [] # Return empty on error
    return leads

@app.route('/api/non_volunteers', methods=['GET'])
def get_non_volunteers():
    leads = read_leads()
    non_volunteers = [
        {"nombre": lead["Nombre"], "email": lead["Email"]}
        for lead in leads
        if lead.get("Voluntario Organizador", "").lower() == "no"
    ]
    return jsonify(non_volunteers)

@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    leads = read_leads()
    volunteers = [
        {"nombre": lead["Nombre"], "email": lead["Email"]}
        for lead in leads
        if lead.get("Voluntario Organizador", "").lower() == "sí" # Using 'sí' as stored previously
    ]
    return jsonify(volunteers)

@app.route('/api/participant_count', methods=['GET'])
def get_participant_count():
    leads = read_leads()
    if not leads:
        return jsonify({"count": 1, "error": "No data found or error reading CSV"})

    unique_emails = set()
    for lead in leads:
        if lead.get("Email"): # Check if email exists
            unique_emails.add(lead["Email"])

    return jsonify({"count": len(unique_emails) + 1})

if __name__ == '__main__':
    # Make sure leads.csv exists for basic testing if run directly
    if not os.path.exists(LEADS_CSV_PATH):
        print(f"Warning: {LEADS_CSV_PATH} not found. API endpoints might return empty data.")
        # Optionally, create a dummy leads.csv for local testing without the main app
        # with open(LEADS_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(['Nombre', 'Email', 'Voluntario Organizador'])
        #     writer.writerow(['Test User No', 'testno@example.com', 'No'])
        #     writer.writerow(['Test User Yes', 'testyes@example.com', 'Sí'])

    app.run(host='0.0.0.0', port=5001, debug=True)

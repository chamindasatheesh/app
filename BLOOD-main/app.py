from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'blood_donation.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS blood_bank (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hospital_name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        blood_group TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        donor_name TEXT NOT NULL,
                        donation_date DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
        conn.commit()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Get blood stock data
        cursor.execute('''SELECT blood_group, hospital_name, location, quantity, donor_name 
                          FROM blood_bank''')
        blood_rows = cursor.fetchall()
        
        # Get donor history data
        cursor.execute('''SELECT donor_name, blood_group, hospital_name, location, quantity, donation_date 
                          FROM blood_bank ORDER BY donation_date DESC''')
        donor_rows = cursor.fetchall()

    # Organize data for templates
    blood_data = {}
    for row in blood_rows:
        bg = row[0]
        if bg not in blood_data:
            blood_data[bg] = []
        blood_data[bg].append({
            'hospital': row[1],
            'location': row[2],
            'quantity': row[3],
            'donor_name': row[4]
        })

    return render_template('combined.html',
                         blood_data=blood_data,
                         donors=donor_rows)

@app.route('/update_blood', methods=['POST'])
def update_blood():
    hospital = request.form['hospital_name']
    location = request.form['location']
    blood_group = request.form['blood_group']
    quantity = request.form['quantity']
    donor = request.form['donor_name']

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''INSERT INTO blood_bank 
                      (hospital_name, location, blood_group, quantity, donor_name)
                      VALUES (?, ?, ?, ?, ?)''',
                   (hospital, location, blood_group, quantity, donor))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/delete_blood', methods=['POST'])
def delete_blood():
    hospital = request.form['hospital_name']
    blood_group = request.form['blood_group']
    donor = request.form['donor_name']

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''DELETE FROM blood_bank 
                      WHERE hospital_name = ? 
                      AND blood_group = ?
                      AND donor_name = ?''',
                   (hospital, blood_group, donor))
        conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
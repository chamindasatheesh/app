from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = 'blood_donation.db'

# Home page to display available blood groups and donor names
@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT blood_bank.blood_group, blood_bank.hospital_name, blood_bank.location, blood_bank.quantity, blood_bank.donor_name
            FROM blood_bank
        """)
        data = cursor.fetchall()

    # Organize data for display
    blood_data = {}
    for row in data:
        blood_group, hospital, location, quantity, donor_name = row
        if blood_group not in blood_data:
            blood_data[blood_group] = []
        blood_data[blood_group].append({
            'hospital': hospital,
            'location': location,
            'quantity': quantity,
            'donor_name': donor_name
        })

    return render_template('index.html', blood_data=blood_data)


# Page to update the blood stock
@app.route('/update_blood_page')
def update_blood_page():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Fetch blood data for the available stock
        cursor.execute("""
            SELECT blood_group, hospital_name, location, quantity, donor_name
            FROM blood_bank
        """)
        data = cursor.fetchall()

    # Organize blood data
    blood_data = {}
    for row in data:
        blood_group, hospital, location, quantity, donor_name = row
        if blood_group not in blood_data:
            blood_data[blood_group] = []
        blood_data[blood_group].append({
            'hospital': hospital,
            'location': location,
            'quantity': quantity,
            'donor_name': donor_name
        })

    return render_template('update_blood.html', blood_data=blood_data)


# Handle updating blood stock
@app.route('/update_blood', methods=['GET', 'POST'])
def update_blood():
    if request.method == 'POST':
        # Get form data
        hospital_name = request.form['hospital_name']
        location = request.form['location']
        blood_group = request.form['blood_group']
        quantity = request.form['quantity']
        donor_name = request.form['donor_name']

        # Update the blood data in your database
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Insert the blood info into the blood_bank table
            cursor.execute('''INSERT INTO blood_bank (hospital_name, location, blood_group, quantity, donor_name) 
                              VALUES (?, ?, ?, ?, ?)''', 
                              (hospital_name, location, blood_group, quantity, donor_name))
            conn.commit()

        return redirect('/update_blood_page')

    # GET request: Display current available blood
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Fetch available blood data
        cursor.execute('''SELECT blood_group, hospital_name, location, quantity, donor_name FROM blood_bank''')
        blood_data = cursor.fetchall()

    # Organize blood data
    blood_data_dict = {}
    for row in blood_data:
        blood_group, hospital, location, quantity, donor_name = row
        if blood_group not in blood_data_dict:
            blood_data_dict[blood_group] = []
        blood_data_dict[blood_group].append({
            'hospital': hospital,
            'location': location,
            'quantity': quantity,
            'donor_name': donor_name
        })

    return render_template('update_blood.html', blood_data=blood_data_dict)


# Route to handle deleting a blood group entry
@app.route('/delete_blood', methods=['POST'])
def delete_blood():
    data = request.form
    hospital_name = data['hospital_name']
    blood_group = data['blood_group']

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Delete the blood group entry from blood_bank
        cursor.execute("DELETE FROM blood_bank WHERE hospital_name = ? AND blood_group = ?", (hospital_name, blood_group))
        conn.commit()

    return jsonify({"status": "success", "message": f"Blood group {blood_group} deleted from {hospital_name}."})

if __name__ == '__main__':
    app.run(debug=True)


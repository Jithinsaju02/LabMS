from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy credentials for testing
USER_CREDENTIALS = {
    "admin": "password123"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            return f"Welcome, {username}! You have successfully logged in."
        else:
            return "Invalid credentials. Please try again.", 401
    return render_template('login.html')

@app.route('/land')
def land():
    return render_template('index.html')





# Mock equipment data
equipment_list = [
    {"id": 1, "name": "Lenovo Laptop 10", "type": "Laptop", "status": "Available"},
    {"id": 2, "name": "Lenovo Laptop 11", "type": "Laptop", "status": "Available"},
    {"id": 3, "name": "Lenovo Laptop 12", "type": "Laptop", "status": "Available"},
    {"id": 4, "name": "Lenovo Laptop 13", "type": "Laptop", "status": "Available"},
]

@app.route('/equipment')
def equipment():
    return render_template('equipment.html', equipment_list=equipment_list)

@app.route('/book/<int:equipment_id>', methods=['GET', 'POST'])
def book_equipment(equipment_id):
    # Find the equipment to book
    equipment = next((e for e in equipment_list if e["id"] == equipment_id), None)
    if not equipment:
        return "Equipment not found", 404

    if request.method == 'POST':
        # Handle form submission and update status
        person_name = request.form['name']
        person_contact = request.form['contact']
        take_time = request.form['take_time']
        return_time = request.form['return_time']
        equipment["status"] = "In Use"
        # Optionally, you can log or store the booking details here
        print(f"Equipment '{equipment['name']}' booked by {person_name} (Contact: {person_contact}) from {take_time} to {return_time}")
        return redirect(url_for('equipment'))

    return render_template('book_equipment.html', equipment=equipment)

@app.route('/return/<int:equipment_id>', methods=['GET', 'POST'])
def return_equipment(equipment_id):
    # Find the equipment to return
    equipment = next((e for e in equipment_list if e["id"] == equipment_id), None)
    if not equipment:
        return "Equipment not found", 404

    # Change the status back to available
    if equipment["status"] == "In Use":
        equipment["status"] = "Available"
        # Optionally, you can log or store the return details here
        print(f"Equipment '{equipment['name']}' is now available.")
    
    return redirect(url_for('equipment'))


if __name__ == '__main__':
    app.run(debug=True)

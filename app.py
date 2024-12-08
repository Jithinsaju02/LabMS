from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'MITS@321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Push the application context to make the current app active
# and create all database tables defined by the SQLAlchemy models
app.app_context().push()
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    


@app.route('/')
def home():
    return render_template('login.html')



@app.route('/land')
@login_required
def land():
    return render_template('index.html')

@app.route('/booklab')
@login_required
def booklab():
    return render_template('booklab.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('land'))
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user:
            flash("User already exists")
            return redirect(url_for('signup'))
        new_user = Users(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))






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

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

class Labsd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    labname = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    from_time = db.Column(db.String(20), nullable=False)
    to_time = db.Column(db.String(20), nullable=False)
    purpose = db.Column(db.String(20), nullable=False)

class Equipments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipmentname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100))
    date = db.Column(db.String(20))
    take_time = db.Column(db.String(20))
    return_time = db.Column(db.String(20))
    status = db.Column(db.String(20))
    

# Push the application context to make the current app active
# and create all database tables defined by the SQLAlchemy models
app.app_context().push()
db.create_all()


equipment_list = [
    {"id": 1, "equipmentname": "Projector", "status": "Available"},
    {"id": 2, "equipmentname": "Laptop 1", "status": "Available"},
    {"id": 3, "equipmentname": "Laptop 2", "status": "Available"},
    {"id": 4, "equipmentname": "Extention", "status": "Available"}
]

if not Equipments.query.first():
    for equipment in equipment_list:
        new_equipment = Equipments(
            id=equipment["id"],
            equipmentname=equipment["equipmentname"],
            status=equipment["status"]
        )
        db.session.add(new_equipment)
    db.session.commit()

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

@app.route('/booklab',methods=['GET','POST'])
@login_required
def booklab():
    if request.method == 'POST':
        username = request.form['username']
        lab = request.form['lab']
        date = request.form['date']
        from_time = request.form['from_time']
        to_time = request.form['to_time']
        purpose = request.form['purpose']
        labs = Labsd.query.filter_by(username=username).first()
        conflicting_booking = Labsd.query.filter_by(labname=lab, date=date).filter(
            (Labsd.from_time <= from_time) & (Labsd.to_time > from_time) |
            (Labsd.from_time < to_time) & (Labsd.to_time >= to_time) |
            (Labsd.from_time >= from_time) & (Labsd.to_time <= to_time)
        ).first()
        if conflicting_booking:
            flash("Lab is already booked for the given time slot")
            return redirect(url_for('booklab'))
        new_user = Labsd(username=username, labname=lab, date=date, from_time=from_time,  to_time= to_time, purpose=purpose
                         )
        db.session.add(new_user)
        db.session.commit()
        flash("lab booked successfully")
        return redirect(url_for('land'))
    return render_template('booklab.html')

@app.route('/bookequipment/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def bookequipment(equipment_id):
    # Fetch equipment from the database
    equipment = Equipments.query.get_or_404(equipment_id)
    
    if request.method == 'POST':
        # Handle form submission
        equipment.booked_by = request.form['name']
        equipment.date = request.form['date']
        equipment.take_time = request.form['take_time']
        equipment.return_time = request.form['return_time']
        equipment.status = "In Use"
        db.session.commit()
        flash(f"Equipment '{equipment.equipmentname}' booked successfully!")
        return redirect(url_for('equipment'))

    return render_template('book_equipment.html', equipment=equipment)

@app.route('/return/<int:equipment_id>', methods=['GET', 'POST'])
def return_equipment(equipment_id):
    # Find the equipment to return
    equipment = Equipments.query.get(equipment_id)
    if not equipment:
        return "Equipment not found", 404

    # Change the status back to available
    if equipment.status == "In Use":
        equipment.status = "Available"
        db.session.commit()
        # Optionally, you can log or store the return details here
        # print(f"Equipment '{equipment['name']}' is now available.")
    
    return redirect(url_for('equipment'))

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










@app.route('/equipment')
@login_required
def equipment():
    equipment_list = Equipments.query.all()
    return render_template('equipment.html', equipment_list=equipment_list)




if __name__ == '__main__':
    app.run(debug=True)

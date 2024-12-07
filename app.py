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

@app.route('/equipment')
def equipment():
    return render_template('equipment.html')

if __name__ == '__main__':
    app.run(debug=True)

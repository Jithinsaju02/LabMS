from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/land')
def land():
    return render_template('home.html')

app.run()
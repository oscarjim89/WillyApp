from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

path = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def index():
    return render_template('Willy.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

#Import required libraries
from flask import Flask, send_from_directory, abort, render_template
import random
import os 

#Initialize Flask app
app = Flask(__name__)
fishtank = 'images'

#Random fish API Endpoint 
@app.route('/fish/')
def serve_image():
    try: 
        random_integer = random.randint(1, 2)
        return send_from_directory(fishtank, f'{random_integer}.jpg')
    except FileNotFoundError:
        abort(404)

#Home page web app route
@app.route('/')
def index():
    return render_template('index.html')

#About page web app rout
@app.route('/about/')
def about():
    return render_template('about.html')

#Run the app
if __name__ == '__main__':
    os.makedirs(fishtank, exist_ok=True) # Make img directory if it doesnt exist, need a tank for da fish
    app.run #(debug=True) Run in debug mode for development
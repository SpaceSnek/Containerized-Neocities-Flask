#Import required libraries
from flask import Flask, send_from_directory, abort, render_template
import random, os, requests, json

#Initialize Flask app
app = Flask(__name__)
fishtank = 'images'
#===== Helper Functions =====#
#Function to get a random dog fact from Dog API
def dogFactFunction():
    APIResponse = requests.get("https://dogapi.dog/api/v2/facts?limit=1")
    data = json.dumps(APIResponse.json())
    parse_json = json.loads(data)
    fact = f"Dog Fact: {parse_json['data'][0]['attributes']['body']}"
    return fact
#===== End Helper Functions =====#

#===== Establish Routing points =====#
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
    dogFact = dogFactFunction()
    return render_template('index.html', dogFact=dogFact)

#About page web app rout
@app.route('/about/')
def about():
    return render_template('about.html')

#Blank page web app route
@app.route('/blank/')
def blank():
    return render_template('blank.html')
#===== End Routing points =====#

#Run the app
if __name__ == '__main__':
    os.makedirs(fishtank, exist_ok=True) # Make img directory if it doesnt exist, need a tank for da fish
    app.run (debug=True) #Run in debug mode for development
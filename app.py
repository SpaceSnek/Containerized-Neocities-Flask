#Import required libraries
from flask import Flask, send_from_directory, abort, render_template
import random, os, requests, json
from atproto import Client
import credentials

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

def get_bsky_posts():
    client = Client()
    client.login(credentials.username, credentials.password)
    target_handle = 'spacesnek.shrimplybetter.me'

    feed = client.app.bsky.feed.get_author_feed({'actor': target_handle, 'limit': 2})
    formattedPost = []
    for post_view in feed['feed']:
        try:
            record = post_view.post.record
            postText = record.text
            embed = post_view.post.embed
            if hasattr(embed, 'images') and embed.images:
                embed = embed.images[0].thumb
            elif hasattr(embed, 'thumbnail') and embed.thumbnail:
                embed = embed.thumbnail
                postText = postText + " [Video thumbail, find video on bsky]"
            else:
                embed = ""
            author = post_view.post.author.handle
            formattedPost.append((author, postText, embed))
        except KeyError:
            formattedPost = "This post has been deleted or is not displaying properly."
    return formattedPost
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

@app.route('/bsky/')
def bsky():
    posts = get_bsky_posts()
    return render_template('bsky.html', posts=posts)
#===== End Routing points =====#

#Run the app
if __name__ == '__main__':
    os.makedirs(fishtank, exist_ok=True) # Make img directory if it doesnt exist, need a tank for da fish
    app.run (debug=True) #Run in debug mode for development
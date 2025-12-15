# Import required libraries
from flask import Flask, send_from_directory, abort, render_template
import random
import os
import requests
import json
import logging
from cachetools import cached, TTLCache
from atproto import Client

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Constants
FISHTANK_DIR = 'images'
DOG_FACT_URL = "https://dogapi.dog/api/v2/facts?limit=1"
BSKY_TARGET_HANDLE = 'spacesnek.shrimplybetter.me'
REQUEST_TIMEOUT = 5  # Set a sensible timeout for external API calls (in seconds)

try:
    import credentials
except ImportError:
    logging.error("credentials.py not found. Please create it with username and password.")
    pass

DOG_FACT_CACHE = TTLCache(maxsize=1, ttl=60) # Cache the fact for 5 minutes (300 seconds)
BSKY_POSTS_CACHE = TTLCache(maxsize=1, ttl=60) # Cache the posts for 1 minute (60 seconds)


# ===== Helper Functions =====#

# Function to get a random dog fact from Dog API
@cached(DOG_FACT_CACHE)
def get_cached_dog_fact():
    logging.info("Fetching new dog fact from API...")
    try:
        response = requests.get(DOG_FACT_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        data = response.json()
        fact = data['data'][0]['attributes']['body']
        return f"Dog Fact: {fact}"

    except requests.exceptions.RequestException as e:
        logging.error(f"Dog API request failed: {e}")
        return "Dog Fact: Failed to fetch a dog fact due to a network error."
    except (KeyError, IndexError, json.JSONDecodeError):
        logging.error("Dog API response parsing failed.")
        return "Dog Fact: Could not parse the dog fact from the API."

# Function to get BlueSky posts
@cached(BSKY_POSTS_CACHE)
def get_cached_bsky_posts(limit=2):
    logging.info("Fetching new BlueSky posts...")
    try:
        client = Client()
        client.login(credentials.username, credentials.password)

        feed = client.app.bsky.feed.get_author_feed({'actor': BSKY_TARGET_HANDLE, 'limit': limit})
        formatted_posts = []

        for post_view in feed.feed:
            post_data = post_view.post
            try:
                record = post_data.record
                post_text = record.text
                embed_url = ""

                embed = post_data.embed
                if embed:
                    if hasattr(embed, 'images') and embed.images:
                        embed_url = embed.images[0].thumb
                    elif hasattr(embed, 'thumbnail') and embed.thumbnail:
                        embed_url = embed.thumbnail
                        post_text += " [Video thumbnail, find video on bsky]"

                author_handle = post_data.author.handle
                formatted_posts.append((author_handle, post_text, embed_url))
            except AttributeError:
                logging.warning("Skipping a potentially broken or non-standard post.")
                continue

        return formatted_posts

    except Exception as e:
        logging.error(f"Error fetching BlueSky posts: {e}")
        return [("Error", "Could not load posts from BlueSky.", "")]

# Helper function to expose the cached dog fact
def dogFactFunction():
    return get_cached_dog_fact()

# Helper function to expose the cached bsky posts
def get_bsky_posts():
    # Pass argument to the cached function to ensure consistent key generation
    return get_cached_bsky_posts(limit=2)

# ===== End Helper Functions =====#

# ===== Establish Routing points =====#

# Random fish API Endpoint
@app.route('/fish/')
def serve_image():
    try:
        available_files = [f for f in os.listdir(FISHTANK_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not available_files:
            raise FileNotFoundError(f"No images found in the '{FISHTANK_DIR}' directory.")
        random_file = random.choice(available_files)
        return send_from_directory(FISHTANK_DIR, random_file)
    except FileNotFoundError as e:
        logging.error(f"Image serving error: {e}")
        abort(404)

# Home page web app route
@app.route('/')
def index():
    dogFact = dogFactFunction()
    return render_template('index.html', dogFact=dogFact)

# About page web app route
@app.route('/about/')
def about():
    return render_template('about.html')

# Blank page web app route
@app.route('/blank/')
def blank():
    return render_template('blank.html')

@app.route('/bsky/')
def bsky():
    posts = get_bsky_posts()
    return render_template('bsky.html', posts=posts)

# ===== End Routing points =====#

# Run the app
if __name__ == '__main__':
    os.makedirs(FISHTANK_DIR, exist_ok=True)
    # Pre-warm caches
    DOG_FACT_CACHE.clear()
    get_cached_dog_fact()
    BSKY_POSTS_CACHE.clear()
    get_cached_bsky_posts(limit=2)

    app.run(debug=True)
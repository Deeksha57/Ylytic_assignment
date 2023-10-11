from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Base URL of the YouTube comments API
BASE_URL = "https://app.ylytic.com/ylytic/test"


@app.route('/')
def home():
    return "Welcome to the Flask API!"


@app.route('/search', methods=['GET'])
def search_comments():
    # Parse query parameters from the request
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    # Make a request to the YouTube comments API
    response = requests.get(BASE_URL)
    comments = response.json()

    # Filter comments based on search criteria
    filtered_comments = []


    for comment in comments:
        if (not search_author or search_author in comment['author']) and \
           (not at_from or at_from <= comment['at'] <= at_to) and \
           (not like_from or like_from <= comment['like'] <= like_to) and \
           (not reply_from or reply_from <= comment['reply'] <= reply_to) and \
           (not search_text or search_text in comment['text']):
            filtered_comments.append(comment)

# Return the filtered comments as a JSON response
    return jsonify(filtered_comments)


if __name__ == '__main__':
    app.run(debug=True)

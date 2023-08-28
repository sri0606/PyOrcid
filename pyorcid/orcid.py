import requests
from flask import Flask, redirect, request
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access the environment variable
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

redirect_uri="http://localhost:5000/callback"
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, this is your temporary server!"

@app.route('/callback')
def callback():
    authorization_code = request.args.get('code')
    
    # Exchange authorization code for access token
    token_url = 'https://orcid.org/oauth/token'
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url, data=token_data)
    token_info = response.json()
    access_token = token_info['access_token']
    
    # Use the access token to make API requests
    headers = {'Authorization': f'Bearer {access_token}'}
    api_url = 'https://pub.orcid.org/v3.0/0000-0002-1825-0097/record'
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return "Retrieved data: " + str(data)
    else:
        return "Failed to retrieve data. Status code: " + str(response.status_code)

if __name__ == '__main__':
    app.run()

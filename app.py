from flask import *
import requests
import time
from functools import wraps
import json

base_api_url = "https://api.uidesign.ai/"

app = Flask(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        
        if 'access_token' in request.cookies:
            access_token = request.cookies.get('access_token')
            refresh_token = request.cookies.get('refresh_token')
            expires_in = int(request.cookies.get('expires_in'))

        if not access_token :
            return redirect("/login")
        
        # returns the current logged in users context to the routes
        return  f(*args, **kwargs)
  
    return decorated
        
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else :
        # GET credentials from client
        email = request.form["email"]
        password = request.form["password"]
        data = {
            'email': email,
            'password': password
        }
        url = base_api_url + 'auth/noflow/login'
        response = requests.post(url, json=data)
        status_code = response.status_code
        res = response.json()
        if status_code == 200:
            token = {
                "access_token": res['access_token'],
                "refresh_token": res['refresh_token'],
                "expires_in": res['expires_in']
            }
            access_token = res['access_token']
            refresh_token = res['refresh_token']
            expires_in = res['expires_in']
           
            resp = make_response(render_template('index.html'))
            resp.set_cookie('access_token', access_token)
            resp.set_cookie('refresh_token', refresh_token)
            now = round(time.time())
            # expires_in += now
            expires_in = now + 3
            resp.set_cookie('expires_in', str(expires_in))
            
            return resp
        return render_template("login.html")

@app.route("/")
@token_required
def dashboard():
    return render_template("index.html")

@app.route("/createproject")
@token_required
def create_project():
    try:
        now = round(time.time())
        access_token = request.cookies.get('access_token')
        refresh_token = request.cookies.get('refresh_token')
        expires_in = int(request.cookies.get('expires_in'))
        if expires_in < now:
            # Get token by refresh_token
            token = refresh(refresh_token)

            resp = make_response(render_template('create.html'))
            resp.set_cookie('access_token', token["access_token"])
            resp.set_cookie('refresh_token', token["refresh_token"])
            now = round(time.time())
            expires_in = token["expires_in"]
            # expires_in += now
            expires_in = now + 3
            resp.set_cookie('expires_in', str(expires_in))
            
            return resp
    except:
        return redirect("/login")

def refresh(refresh_token):
    url = base_api_url + 'auth/noflow/refresh'
    data = {
        "refresh_token": refresh_token
    }
    response = requests.post(url, json=data)
    status_code = response.status_code

    if status_code == 200:
        return response.json()
    return None

if __name__ == '__main__':
    app.run(debug = False, host='127.0.0.1', port=5000)
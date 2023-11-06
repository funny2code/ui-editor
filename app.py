from flask import *
import requests
import time
from functools import wraps
import json
from flask_cors import CORS

base_api_url = "https://api.uidesign.ai/"

app = Flask(__name__, static_folder='static', static_url_path="/static")
CORS(app)

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
            resp.set_cookie('id_token', token["access_token"])
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



@app.route("/newproject")
def newproject():
    return render_template("index.html")

@app.route("/updateproject", methods=["POST"])
def updateProject():
    project_data = request.json["project_data"]
    project_id = request.json["project_id"]
    refresh_token = request.json["refresh_token"]

    if refresh_token is None:
        return jsonify ({"message": "failed"})

    token = refresh(refresh_token)
    id_token = token["id_token"]
    access_token = token["access_token"]
    refresh_token = token["refresh_token"]
    headers = {
        'Authorization': 'Bearer ' + id_token,
        'Content-Type': 'application/json'
    }

    # print(project_data)
    # print(project_id)
    # print(id_token)
    url = base_api_url + f"v2/user/projects/{project_id}"
    response = requests.put(url, headers=headers, json = project_data)
    print(response)
    return jsonify({"message": "success"})

@app.route("/display", methods=["POST"])
def displayProject():
    refresh_token = request.json["refresh_token"]
    token = refresh(refresh_token)
    id_token = token["id_token"]
    access_token = token["access_token"]
    refresh_token = token["refresh_token"]
    action = request.json["action"]

    headers = {
        'Authorization': 'Bearer ' + id_token,
        'Content-Type': 'application/json'
    }

    if action == "edit_project":
        project_id = request.json["project_id"]
        url = f"https://api.uidesign.ai/v2/user/projects/{project_id}"
        project_data = requests.get(url, headers=headers).json()
        pages_data = project_data["result"][0]["context"]
        print(pages_data)
        return render_template("create.html", project_data=project_data, id_token=id_token, project_id=project_id, access_token=access_token, refresh_token=refresh_token)
        
    elif action == "create_project":
        url = "https://api.uidesign.ai/v2/user/projects/"
        project_data = request.json["data"]
        created_project = requests.post(url, json=project_data, headers=headers).json()
        project_id = created_project["id"]
        return render_template("create.html", project_data=project_data, id_token=id_token, project_id=project_id, access_token=access_token, refresh_token=refresh_token)

if __name__ == '__main__':
    app.run(debug = False, host='127.0.0.1', port=5000)
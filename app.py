from flask import *
import requests

base_api_url = "https://api.uidesign.ai/"

app = Flask(__name__)

@app.before_request
def hook():
    print("endpoint: %s, url: %s, path: %s, method: %s" % (request.endpoint, request.url, request.path, request.method))
    # if request.path == "/":
    #     print(request.method)
    #     return redirect("/login")
    
    if request.path == '/login' and request.method == "POST":        
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
        response_body = response.json()

        print(type(status_code))
        print("response_body", response_body)

        if status_code == 200:
            print("PASSED")
            return redirect(url_for('.dashboard', response_body=response_body))
        
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else :
        email = request.form["email"]
        password = request.form["password"]
        return redirect("/")

@app.route("/")
def dashboard():
    print(request.args['response_body'])
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = False, host='127.0.0.1', port=5000)
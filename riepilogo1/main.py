
from flask import Flask, render_template, request, redirect, url_for
import json




from flask import Flask,redirect,url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from google.cloud import firestore


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.carrello_spesa = []

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# The login manager contains the code that lets your application and Flask-Login work together,
# such as how to load a user from an ID, where to send users when they need to log in, and the like.
login = LoginManager(app)
login.login_view = '/static/login.html'


usersdb = {
    'marco':'mamei'
}

@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None


db = 'test1'
db = firestore.Client.from_service_account_json('riepilogo1/credentials.json', database=db)

@app.route('/graph/<sensor>')
def graph(sensor):
    entity = db.collection('sensors').document(sensor).get()
    if entity.exists:
        x = entity.to_dict()['readings']
        x2 = []
        for d in x:
            x2.append([d['data'], d['val']])
        x = str(x2)
        return render_template('graph.html', data=x, sensor=sensor)    
    else:
        return 'not found', 404

# parameters in the url
@app.route('/sensors/<sensor>',methods=['GET'])
def read(sensor):
    entity = db.collection('sensors').document(sensor).get()
    if entity.exists:
        d = entity.to_dict()
        return json.dumps(d['readings']), 200
    else:
        return 'not found', 404

# http get parameters
@app.route('/sensors/<sensor>',methods=['POST'])
def new_data(sensor):
    data = request.values['date']
    val = float(request.values['val'])

    
    entity = db.collection('sensors').document(sensor).get()
    if entity.exists:
        d = entity.to_dict()
        d['readings'].append({'data':data, 'val':val})
        db.collection('sensors').document(sensor).set(d)
    else:
        db.collection('sensors').document(sensor).set({'readings':[{'data':data, 'val':val}]})
    return 'ok', 200


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/main')
    username = request.values['u']
    password = request.values['p']
    next_page = request.values['next']
    if username in usersdb and password == usersdb[username]:
        login_user(User(username))
        if not next_page:
            next_page = '/main'
        return redirect(next_page)
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


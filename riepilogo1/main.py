
from flask import Flask, render_template, request, redirect, url_for
import json
from joblib import load
from flask import Flask,redirect,url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from google.cloud import firestore, storage
import time
from datetime import datetime, timedelta

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




@login.user_loader
def load_user(username):
    entity = db.collection('users').document(username).get()
    if entity.exists:
        return User(username)
    return None

db = 'test1'
db = firestore.Client.from_service_account_json('riepilogo1/credentials.json', database=db)
filestorage = storage.Client.from_service_account_json('riepilogo1/credentials.json')


@app.route('/')
@login_required
def main():
    return redirect('/static/map.html')



@app.route('/getmap')
@login_required
def getmap():
    #time.sleep(10)
    return '[[[44.6,10.7],"sensor1"],[[44.5,10.8],"sensor2"],[[44.4,10.9],"sensor3"]]'

def f_next_date(last_date):
    data = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")
    # Calcolo del giorno successivo
    next_date = data + timedelta(days=1)
    # Conversione di nuovo in stringa
    is_weekend = 1 if next_date.weekday() >= 5 else 0
    return next_date.strftime("%Y-%m-%d %H:%M:%S"), is_weekend


@app.route('/graph/<sensor>')
@login_required
def graph(sensor):
    #time.sleep(10)
    entity = db.collection('sensors').document(sensor).get()
    if entity.exists:
        x = entity.to_dict()['readings']
        x2 = []
        for d in x:
            x2.append([d['data'], d['val']])
        
        model = load('riepilogo1/models/model.joblib') 
        y = []

        next_date1, is_weekend1 = f_next_date(x2[-1][0])
        history = [x2[-1][1],x2[-2][1],x2[-3][1],is_weekend1]
        predictions =[model.predict([history])]
        y.append([next_date1,float(predictions[0][0])])

        next_date2, is_weekend2 = f_next_date(next_date1)
        history = [y[-1][1],x2[-1][1],x2[-2][1],is_weekend2]
        predictions =[model.predict([history])]
        y.append([next_date2,float(predictions[0][0])])


        x2 = x2 + y
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


@app.route('/sensorsfile/<sensor>',methods=['POST'])
def new_file(sensor):
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'missing file', 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return 'missing file name', 400
    
    bucket = filestorage.bucket('upload_pcloud2025')
    source_file_name = file.filename
    destination_blob_name = f'{sensor}_{source_file_name}'
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(file.read(),content_type=file.content_type)

    return f'File {source_file_name} uploaded to {destination_blob_name}', 200

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
    next_page = request.values.get('next', '/main')
    
    # Access Firestore to validate the user
    entity = db.collection('users').document(username).get()
    if entity.exists:
        user_data = entity.to_dict()
        if user_data.get('password') == password:
            login_user(User(username))
            return redirect(next_page)
    
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


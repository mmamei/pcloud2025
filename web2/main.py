
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

database = {'sensor1': [{'data':'27/10/2019', 'val': 23}]}
'''
database = {
'sensor1': [
{data:'27/10/2019', val: 23},
...
]

}
'''

@app.route('/graph/<sensor>')
def graph(sensor):
    if sensor not in database:
        return 'not found', 404
    x = database[sensor]
    x2 = []
    for d in x:
        x2.append([d['data'], d['val']])
    x = str(x2)
    return render_template('graph.html', data=x, sensor=sensor)    

# parameters in the url
@app.route('/sensors/<sensor>',methods=['GET'])
def read(sensor):
    if sensor not in database:
        return 'not found', 404
    x = database[sensor]
    return json.dumps(x), 200

# http get parameters
@app.route('/sensors/<sensor>',methods=['POST'])
def new_data(sensor):
    data = request.values['date']
    val = float(request.values['val'])
    if sensor not in database:
        database[sensor] = []
    database[sensor].append({'data':data, 'val':val})
    return 'ok', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


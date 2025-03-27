
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

database = {}
'''
database = {
'sensor1': [
{data:'27/10/2019', val: 23},
...
]

}
'''


# parameters in the url
@app.route('/urlpar/<par>',methods=['GET'])
def urlpar(par):
    user = {'username': par}
    list = [1, 2, 3, 4, 5]
    return render_template('index.html', title='Home', user=user, list=list)

# http get parameters
@app.route('/sensors/<sensor>',methods=['POST'])
def new_data(sensor):
    data = request.values['date']
    val = request.values['val']
    if sensor not in database:
        database[sensor] = []
    database[sensor].append({'data':data, 'val':val})
    return 'ok', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


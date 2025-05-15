from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    from requests import post
    url = 'https://europe-west8-pcloud2025.cloudfunctions.net/hello_http'
    r = post(url,json={'name':'matteo'})
    print(r.status_code)
    print(r.text)
    return r.text


@app.route('/js',methods=['GET'])
def mainjs():
    return render_template('index_js.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


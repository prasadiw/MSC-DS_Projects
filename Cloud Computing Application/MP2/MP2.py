from flask import request
from flask import abort
from flask import Flask, jsonify

app = Flask(__name__)

counter = 0

@app.route('/', methods=['POST'])
def test_post_number():
    global counter
    content = request.get_json()
    counter = content['num']
    return str(counter)

@app.route('/', methods=['GET'])
def test_number():
    global counter
    return str(counter)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

from flask import Flask, Response, jsonify

app = Flask(__name__)

@app.route('/update')
def update(data: dict):
    graph = jsonify(data)
    return Response(status=200)

app.run(debug=True)
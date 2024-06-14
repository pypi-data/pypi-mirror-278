from flask import Flask, render_template, request, jsonify
from .decision_engine import DecisionEngine, Inquiry

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    engine = DecisionEngine()
    engine.declare(Inquiry(sentence=data['text']))
    engine.run()
    return jsonify(response=engine.response)

def create_app():
    return app

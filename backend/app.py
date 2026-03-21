from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"message": "Mechanical Engineering API is running"}

@app.route('/stress', methods=['POST'])
def stress():
    data = request.json
    force = float(data['force'])
    area = float(data['area'])
    return jsonify({'stress': force / area})

@app.route('/strain', methods=['POST'])
def strain():
    data = request.json
    delta_length = float(data['delta_length'])
    original_length = float(data['original_length'])
    return jsonify({'strain': delta_length / original_length})

@app.route('/youngs_modulus', methods=['POST'])
def youngs_modulus():
    data = request.json
    stress = float(data['stress'])
    strain = float(data['strain'])
    return jsonify({'youngs_modulus': stress / strain})

if __name__ == '__main__':
    app.run(debug=True)
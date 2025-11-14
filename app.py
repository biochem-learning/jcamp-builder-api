from flask import Flask, request
from flask_cors import CORS
from process import build_jcamp, build_jcamp_blocks, build_metadata, build_assignment_table
from scipy.signal import find_peaks
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def testing_route():
    return '<h1>Flask App is currently running</h1>'
    

@app.route('/build_jcamp', methods=['POST'])
def build_jcamp_route():
    data = request.json
    metadatas_dict = data.get('metadatas', {})
    assignments_list = data.get('assignments', [])
    spec_jcamp = data.get('specJcamp', '')
    struc_jcamp = data.get('strucJcamp', '')

    spec_bloc = build_jcamp_blocks(spec_jcamp, 4)
    struc_bloc = build_jcamp_blocks(struc_jcamp, 1)

    metadatas = build_metadata(metadatas_dict)
    assign_table = build_assignment_table(assignments_list)

    built_jcamp = build_jcamp(metadatas, struc_bloc, spec_bloc, assign_table)

    return built_jcamp

@app.route('/find_peak', methods=['POST'])
def find_peak_route():
    data = request.json
    array = data.get('array', [])
    prominence = data.get('prominence', None)
    
    peaks, _ = find_peaks(array, prominence)
    return peaks


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    
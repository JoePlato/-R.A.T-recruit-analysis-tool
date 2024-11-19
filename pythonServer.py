import recruitAnalysis

from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/get_thresholds', methods=['GET'])
def get_thresholds():
    # Example values
    file_path = request.args.get('filePath')
    
    if file_path:

        # Process the file path here
        # For example, print it or perform some action
        player_results = recruitAnalysis.math_stuff(file_path)
        return jsonify({
            'results': player_results
        })
    else:
        return "No file path provided", 400
    # Return as JSON
    

if __name__ == '__main__':
    app.run(debug=True)

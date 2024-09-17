from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Dictionary to store file metadata (filename -> storage node address)
file_metadata = {}

# Endpoint to register a new file with its storage node address
@app.route('/add_file', methods=['POST'])
def add_file():
    # Expecting JSON data with 'filename' and 'storage_node'
    data = request.json
    filename = data.get('filename')
    storage_node = data.get('storage_node')
    
    if not filename or not storage_node:
        return jsonify({"error": "Filename and storage node are required."}), 400

    # Store the file metadata
    file_metadata[filename] = storage_node

    return jsonify({"message": f"File '{filename}' added successfully.", "storage_node": storage_node}), 200

# Endpoint to retrieve the storage node address for a requested file
@app.route('/get_file', methods=['GET'])
def get_file():
    # Retrieve the filename from the query parameters
    filename = request.args.get('filename')
    
    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    # Look for the filename in the metadata dictionary
    storage_node = file_metadata.get(filename)
    
    if storage_node:
        return jsonify({"filename": filename, "storage_node": storage_node}), 200
    else:
        return jsonify({"error": f"File '{filename}' not found."}), 404

# Start the Flask server
if __name__ == '__main__':
    # The metadata server will run on port 5000 by default
    app.run(port=5000)

from flask import Flask, request, send_from_directory, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# Directory where files will be stored
UPLOAD_DIRECTORY = "E:/Projects/Academics/Distributed-System/meta_data_&_storage_node/Server/Server-storage"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Endpoint to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Path where the file will be saved
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    print(f"Saving file to: {file_path}")  # <-- Add this line to check the file path

    file.save(file_path)

    return jsonify({"message": f"File '{file.filename}' uploaded successfully"}), 200

# Endpoint to handle file downloads
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Serve the file if it exists in the upload directory
    try:
        return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

# Start the Flask server
if __name__ == '__main__':
    app.run(port=6000)  # Running on port 6000

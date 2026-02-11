

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VALID_API_KEY = os.getenv("API_KEY")

# POINT THIS TO YOUR ACTUAL FOLDER
UPLOAD_FOLDER = r"uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_valid_api_key():
    # Try header first
    api_key = request.headers.get("x-api-key")

    # If not in header, try URL query parameter (for Chrome testing)
    if not api_key:
        api_key = request.args.get("api_key")

    print("Received API Key:", api_key)
    print("Expected API Key:", VALID_API_KEY)

    return api_key == VALID_API_KEY


# -------- READ ALL FILES --------
@app.route("/read-all-files", methods=["GET"])
def read_all_files():

    if not is_valid_api_key():
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    files = os.listdir(UPLOAD_FOLDER)

    if not files:
        return jsonify({"error": "No files found in uploads folder"}), 404

    all_files_data = []

    for filename in files:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading file: {str(e)}"

        all_files_data.append({
            "filename": filename,
            "stored_path": file_path,
            "content": content
        })

    return jsonify({
        "total_files": len(files),
        "files": all_files_data
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)



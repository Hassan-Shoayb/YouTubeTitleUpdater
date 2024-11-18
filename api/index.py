from flask import Flask, jsonify
from App import update_video_title  # Adjust the import if necessary

app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        update_video_title("YOUR_VIDEO_ID")
        return jsonify({"message": "Title updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
from flask import Flask, request, jsonify
from src.file_upload.file_upload import upload, create_upload_folder
from src.publish_queue.publish import create_queue_connection, publish_message


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    response_json, response_code = upload(request)

    if response_code == 200:
        video_path = response_json['path'] 
        video_id = response_json['id']
        body = {"video_path":video_path, "video_id": video_id}
        publish_message(rabbit_connection, body)

    return jsonify([response_json,response_code])

if __name__ == '__main__':
    create_upload_folder()
    global rabbit_connection
    rabbit_connection = create_queue_connection()
    app.run(debug=True, host='0.0.0.0', port=5000)

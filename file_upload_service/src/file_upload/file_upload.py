import os
import uuid
from werkzeug.utils import secure_filename

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}


def create_upload_folder():
    """Create the upload folder if it doesn't exist."""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload(request):
    """Handle file upload."""
    if 'file' not in request.files:
        return {"error": "No file part","id":"","path":""}, 400

    file = request.files['file']
    
    if file.filename == '':
        return {"error": "No selected file","id":"","path":""}, 400

    if file and allowed_file(file.filename):
        video_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)  # Use secure_filename for security
        extension = '.' in filename and filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(UPLOAD_FOLDER,f"{video_id}.{extension}")
        print(filepath)
        try:
            file.save(filepath)
        except IOError as e:
            return {"error": "Could not save file","id":"","path":""}, 500
        return {"message": "File uploaded successfully", "filename": filename,"id":video_id,"path":os.path.join(os.getcwd(),filepath)}, 200

    return {"error": "File type not allowed","id":"","path":""}, 400
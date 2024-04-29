from flask import Flask, request, send_file, send_from_directory, url_for
from flask_restful import Api, Resource
import os
from werkzeug.utils import secure_filename
import uuid
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

# Function to check if the uploaded file is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Resource for uploading images
class UploadImage(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}
        
        file = request.files['file']

        if file.filename == '':
            return {'error': 'No selected file'}

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Generate unique filename
            unique_filename = str(uuid.uuid4())[:8] + '_' + filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            image = Image(filename=unique_filename)
            db.session.add(image)
            db.session.commit()

            public_url = url_for('serve_static', filename=unique_filename, _external=True)

            return {'message': 'File uploaded successfully', 'filename': unique_filename, 'url': public_url, 'face': image.id}
        else:
            return {'error': 'File type not allowed'}
        
class DeleteImage(Resource):
    def delete(self, image_id):
        image = Image.query.get(image_id)
        if image:
            # Delete the corresponding file from the filesystem
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            if os.path.exists(image_path):
                os.remove(image_path)
            return {'message': 'Image deleted successfully'}
        else:
            return {'error': 'Image not found'}, 404

# Resource for retrieving image by filename
class GetImage(Resource):
    def get(self, filename):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(image_path):
            return send_file(image_path)
        else:
            return {'error': 'Image not found'}, 404

# Adding resources to the API
api.add_resource(UploadImage, '/upload')
api.add_resource(GetImage, '/image/<string:filename>')
api.add_resource(DeleteImage, '/delete/<int:image_id>')

# Route to serve static files (uploaded images)
@app.route('/uploads/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=9000, debug=True)

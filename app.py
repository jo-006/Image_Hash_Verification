import hashlib
from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database to store original image hashes
# In a real application, this would be a proper database
IMAGE_HASHES = {
    # Format: 'image_name.jpg': 'hash_value'
}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def calculate_hash(file_path):
    """Calculate SHA-256 hash of an image file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read and update hash in chunks for memory efficiency
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_sha256.update(byte_block)
    return hash_sha256.hexdigest()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register_original():
    """Register an original image and store its hash"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Calculate and store hash
        file_hash = calculate_hash(file_path)
        IMAGE_HASHES[filename] = file_hash

        return jsonify({
            'message': 'Original image registered successfully',
            'filename': filename,
            'hash': file_hash
        })

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/verify', methods=['POST'])
def verify_image():
    """Verify if an uploaded image matches its original hash"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Check if we have a record of this image
        if filename not in IMAGE_HASHES:
            return jsonify({'error': 'Unknown image. Please register the original first'}), 400

        # Save temporarily to calculate hash
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_' + filename)
        file.save(temp_path)

        # Calculate hash
        uploaded_hash = calculate_hash(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        # Compare hashes
        original_hash = IMAGE_HASHES[filename]
        if uploaded_hash == original_hash:
            return jsonify({
                'verified': True,
                'message': 'Image verified successfully. No alterations detected.',
                'original_hash': original_hash,
                'uploaded_hash': uploaded_hash
            })
        else:
            return jsonify({
                'verified': False,
                'message': 'REJECTED: Image has been altered!',
                'original_hash': original_hash,
                'uploaded_hash': uploaded_hash
            }), 400

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/list', methods=['GET'])
def list_registered():
    """List all registered original images and their hashes"""
    return jsonify({
        'registered_images': {k: v for k, v in IMAGE_HASHES.items()}
    })


if __name__ == '__main__':
    app.run(debug=True)
# Image Hash Verification System

A secure web application for verifying the integrity of digital images through cryptographic hash comparison. This system helps detect if images have been tampered with or altered by comparing their SHA-256 hash values.

## Author

[Joshnitha] - [joshi122006@gmail.com]

## Features

- **Image Registration**: Upload and register original images with their hash values
- **Image Verification**: Check if an image has been modified by comparing it against its original hash
- **Hash Visualization**: View all registered images and their corresponding hash values
- **Intuitive Interface**: Clean, responsive design with visual feedback for verification results
- **Real-time Processing**: Instant hash calculation and verification

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Cryptography**: SHA-256 hashing algorithm
- **File Handling**: Werkzeug for secure file uploads

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-hash-verification.git
cd image-hash-verification
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install flask
```

4. Run the application:
```bash
flask run
```
or
```bash
python app.py
```

5. Access the application at http://localhost:5000

## How It Works

1. **Registration Process**:
   - User uploads an original image
   - System calculates a SHA-256 hash of the image file
   - The filename and hash are stored in the system

2. **Verification Process**:
   - User uploads an image to verify
   - System calculates the hash of the uploaded image
   - The hash is compared with the stored hash of the original image
   - Results show whether the image is unchanged or has been altered

## Project Structure

```
tamperproof/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Frontend interface
└── uploads/            # Storage for temporary image files
```

## Security Considerations

- Uses secure filename handling to prevent path traversal attacks
- Implements memory-efficient hash calculation for large files
- Temporarily stores files for verification and then removes them
- Validates file types to prevent unauthorized file uploads

## Future Enhancements

- Persistent database storage for image hashes
- User authentication system
- Support for additional file formats
- More detailed tampering analysis
- Export/import functionality for hash databases
- Batch processing for multiple files

## Disclaimer

This tool provides basic image verification and is intended for educational purposes. For critical security applications, consider additional verification mechanisms and professional security consultation.

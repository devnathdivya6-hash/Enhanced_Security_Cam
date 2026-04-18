# Security Camera System

A comprehensive Django-based security camera system with face recognition, object detection, violence detection, and intercom features.

## Features

- 👤 **Face Recognition** - Custom-trained LBPH face recognition
- 📦 **Object Detection** - TensorFlow-based object detection
- 😠 **Violence Detection** - LSTM-based video violence detection
- 🎤 **Intercom System** - Voice communication features
- 📧 **Email Alerts** - Automated notifications for security events

## Prerequisites

- Python 3.11+
- FFmpeg (for voice features)
- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd SecurityCam
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv myven
   myven\Scripts\activate  # Windows
   # source myven/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r req.txt
   ```

4. **Setup FFmpeg (for voice features):**
   - Download FFmpeg from: https://github.com/BtbN/FFmpeg-Builds/releases
   - Download: `ffmpeg-master-latest-win64-gpl-shared.zip`
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to your system PATH

## Model Setup

This project uses three ML models:

### 1. Face Recognition Model (Custom-trained)
- **File:** `trained_faces.yml`
- **Training:** Run the face capture and training features in the web interface
- **Size:** ~45MB (generated during training)

### 2. Object Detection Model (Pre-trained)
- **Source:** TensorFlow Object Detection API
- **Download:** Run the setup script or download manually
- **Size:** ~710MB

### 3. Violence Detection Model (Pre-trained)
- **File:** `violence_detection/data/violence_vedio_model.h5`
- **Source:** Pre-trained LSTM model
- **Size:** ~115MB

## Model Download Instructions

### Option 1: Automated Setup (Recommended)
Run the setup script after installation:
```bash
python setup_models.py
```

### Option 2: Manual Download

1. **Object Detection Model:**
   ```bash
   # Download TensorFlow Object Detection model
   # Place in: object/saved_model/
   # You can use any SSD MobileNet model from TensorFlow Model Zoo
   ```

2. **Violence Detection Model:**
   ```bash
   # Download from your model source or cloud storage
   # Place in: violence_detection/data/violence_vedio_model.h5
   ```

## Database Setup

1. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Training Face Recognition

1. Register/Login as a user
2. Go to "Capture Faces" section
3. Capture face images for each person (50 images recommended)
4. The system automatically trains the model

## Project Structure

```
SecurityCam/
├── face/                    # Face recognition app
│   ├── face_utils.py       # Face recognition utilities
│   └── trained_faces.yml   # Face recognition model (generated)
├── object/                 # Object detection app
│   └── saved_model/        # TensorFlow model (download required)
├── violence_detection/     # Violence detection app
│   └── data/
│       └── violence_vedio_model.h5  # Violence model (download required)
├── intercom/               # Voice communication app
├── media/                  # User uploads and outputs
├── static/                 # Static files
├── templates/              # HTML templates
├── myven/                  # Virtual environment (excluded from Git)
├── db.sqlite3             # Database (excluded from Git)
└── req.txt                # Python dependencies
```

## Git Management

### Large Files Handling
- ML models are excluded from Git due to size limits
- Use the provided setup scripts to download models
- Virtual environment is excluded (.gitignore)

### Pushing to Git
```bash
# Add files
git add .

# Commit
git commit -m "Initial commit: Security Camera System"

# Push
git remote add origin <your-repo-url>
git push -u origin main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and security purposes.

## Support

For issues related to:
- **Face Recognition:** Ensure proper lighting and face capture
- **Object Detection:** Verify TensorFlow model is properly loaded
- **Violence Detection:** Check video format compatibility
- **Voice Features:** Ensure FFmpeg is properly installed

## Security Notes

- Change default Django SECRET_KEY in production
- Configure proper email settings for alerts
- Use HTTPS in production
- Regularly backup the database and trained models
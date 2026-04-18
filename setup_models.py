#!/usr/bin/env python
"""
Security Camera Model Setup Script
Downloads required ML models for the security camera system.
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path

def download_file(url, destination):
    """Download a file from URL to destination."""
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {destination}")

def setup_object_detection_model():
    """Setup TensorFlow Object Detection model."""
    print("\n=== Setting up Object Detection Model ===")

    model_dir = Path("object/saved_model")
    if model_dir.exists():
        print("Object detection model already exists. Skipping...")
        return

    # Create directory
    model_dir.mkdir(parents=True, exist_ok=True)

    # Note: You'll need to provide actual download URLs for your models
    print("⚠️  Object detection model needs to be downloaded manually.")
    print("   Please download a TensorFlow Object Detection model and place it in:")
    print("   object/saved_model/")
    print("   Recommended: SSD MobileNet V2 from TensorFlow Model Zoo")

def setup_violence_detection_model():
    """Setup violence detection model."""
    print("\n=== Setting up Violence Detection Model ===")

    model_path = Path("violence_detection/data/violence_vedio_model.h5")
    if model_path.exists():
        print("Violence detection model already exists. Skipping...")
        return

    # Create directory
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Note: You'll need to provide actual download URL for your model
    print("⚠️  Violence detection model needs to be downloaded manually.")
    print("   Please download the violence detection model and place it at:")
    print("   violence_detection/data/violence_vedio_model.h5")

def setup_face_recognition():
    """Setup face recognition (will be trained by user)."""
    print("\n=== Face Recognition Setup ===")
    print("✅ Face recognition will be trained when you use the web interface.")
    print("   Go to 'Capture Faces' in the web app to train the model.")

def main():
    """Main setup function."""
    print("🚀 Security Camera Model Setup")
    print("=" * 40)

    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: Please run this script from the SecurityCam project root directory.")
        return

    try:
        setup_object_detection_model()
        setup_violence_detection_model()
        setup_face_recognition()

        print("\n" + "=" * 40)
        print("✅ Setup complete!")
        print("\nNext steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py runserver")
        print("3. Open: http://127.0.0.1:8000/")
        print("4. Train face recognition through the web interface")

    except Exception as e:
        print(f"❌ Error during setup: {e}")

if __name__ == "__main__":
    main()
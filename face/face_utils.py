from urllib import request
import cv2
import os
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import numpy as np
import csv
import time
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

last_email_time = {}

def send_email(attachment_path=None, name=None):
    current_time = time.time()
    subject = "Unknown Face Detected"
    body = f"An unknown face has been detected at {time.strftime('%Y-%m-%d %H:%M:%S')}."
    to_email = settings.DEFAULT_RECEIVER_EMAIL
                
    
    try:
        # Create email message
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,  # From your configured email
            to=[to_email]  # Recipient email
        )

        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            email.attach_file(attachment_path)

        # Send the email
        email.send()
        # Update last email sent time
        last_email_time[name] = current_time
        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")



def capture_face_with_name(name, image_limit=50):
    face_cascade = cv2.CascadeClassifier('D:/SecurityCam Final/SecurityCam/face/haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)
    
    count = 0
    face_dir = os.path.join('faces', name)
    if not os.path.exists(face_dir):
        os.makedirs(face_dir)
    
    print(f"Capturing up to {image_limit} faces for: {name}")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            count += 1
            face = frame[y:y + h, x:x + w]
            cv2.imwrite(os.path.join(face_dir, f'face_{count}.jpg'), face)  

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= image_limit:
            break
    
    print(f"Captured {count} face images for: {name}.")
    
    video_capture.release()
    cv2.destroyAllWindows()






# def train_faces():
#     face_recognizer = cv2.face.LBPHFaceRecognizer_create()
#     face_cascade = cv2.CascadeClassifier('D:/prjc/hello/Enhanced Security/virtual_env/SecurityCam/face/haarcascade_frontalface_default.xml')

#     faces = []
#     labels = []
#     label_map = {}
#     current_label = 0

#     print("Training faces...")

#     for name in sorted(os.listdir('faces')):  # Sort for consistent ordering
#         person_path = os.path.join('faces', name)
#         if not os.path.isdir(person_path):
#             continue  
        
#         label_map[current_label] = name  
#         print(f"Processing {name}...")

#         for image_filename in os.listdir(person_path):
#             image_path = os.path.join(person_path, image_filename)
#             image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#             if image is None:
#                 print(f"Warning: Unable to read image {image_path}. Skipping.")
#                 continue

#             faces_detected = face_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5)
#             if len(faces_detected) == 0:
#                 print(f"No face detected in image {image_path}. Skipping.")
#                 continue
            
#             (x, y, w, h) = faces_detected[0]
#             face = cv2.resize(image[y:y+h, x:x+w], (200, 200))  # Ensure consistent size
#             faces.append(face)
#             labels.append(current_label)
        
#         current_label += 1
    
#     if len(faces) == 0:
#         print("Error: No faces found for training. Please ensure you have images captured.")
#         return

#     face_recognizer.train(faces, np.array(labels))
#     face_recognizer.save('trained_faces.yml')

#     # Save the label map for consistency
#     with open('label_map.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         for label, name in label_map.items():
#             writer.writerow([label, name])
    
#     print("Training completed. Model saved as 'trained_faces.yml'.")


# def recognize_faces(request):
#     face_recognizer = cv2.face.LBPHFaceRecognizer_create()
#     face_recognizer.read('trained_faces.yml')
    
#     face_cascade = cv2.CascadeClassifier('D:/prjc/hello/Enhanced Security/virtual_env/SecurityCam/face/haarcascade_frontalface_default.xml')
#     video_capture = cv2.VideoCapture(0)

#     # Load label_map from file
#     label_map = {}
#     with open('label_map.csv', mode='r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             label_map[int(row[0])] = row[1]

#     colors = {}

#     def get_color(label):
#         if label not in colors:
#             colors[label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#         return colors[label]

#     while True:
#         ret, frame = video_capture.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
#         for (x, y, w, h) in faces_detected:
#             face_region = gray[y:y+h, x:x+w]
#             face_region_resized = cv2.resize(face_region, (200, 200))  # Resize to match training images
#             label, confidence = face_recognizer.predict(face_region_resized)

#             # Only show "Unknown" for faces with a confidence below a threshold
#             if confidence > 40:  # Adjust confidence threshold
#                 name = label_map.get(label, "Unknown")
#                 confidence_text = f"Confidence: {round(100 - confidence)}%"
#                 face_color = get_color(label)
#             else:
#                 name = "Unknown"
#                 confidence_text = "Confidence too low"
#                 face_color = (0, 0, 255)

#             # Capture screenshot
#             timestamp = time.strftime("%Y%m%d_%H%M%S")
#             screenshot_filename = f'screenshot_{name}_{timestamp}.jpg'
#             screenshot_path = os.path.join('screenshots', screenshot_filename)

#             if not os.path.exists('screenshots'):
#                 os.makedirs('screenshots')

#             cv2.imwrite(screenshot_path, frame)
#             log_to_csv(name, screenshot_path)

#             cv2.rectangle(frame, (x, y), (x + w, y + h), face_color, 2)
#             cv2.putText(frame, f"{name} {confidence_text}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, face_color, 2)

#             # Check if the email was already sent in the last hour
#             current_time = time.time()
#             if name != "Unknown" and (name not in last_email_time or current_time - last_email_time[name] > 3600):
#                 # Send email with the screenshot
#                 subject = f"Face Recognition Alert: {name}"
#                 body = f"A face has been recognized as {name}. Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
#                 to_email = request.user.email # Change this to the email you want to send the alert to
#                 send_email(subject, body, to_email, screenshot_path)

#                 # Update last email sent time
#                 last_email_time[name] = current_time

#             # Handle unknown faces separately
#             if name == "Unknown" and (name not in last_email_time or current_time - last_email_time[name] > 3600):
#                 subject = "Unknown Face Detected"
#                 body = f"An unknown face has been detected at {time.strftime('%Y-%m-%d %H:%M:%S')}."
#                 to_email = request.user.email
#                 send_email(subject, body, to_email, screenshot_path)
                
#                 # Update last email sent time
#                 last_email_time[name] = current_time

#         cv2.imshow('Face Recognition', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     video_capture.release()
#     cv2.destroyAllWindows()


# def log_to_csv(name, screenshot_path):
#     with open('face_log.csv', mode='a', newline='') as file:
#         writer = csv.writer(file)
#         current_time = time.strftime("%Y-%m-%d %H:%M:%S")
#         writer.writerow([name, current_time, screenshot_path])





def train_faces():
    # face_recognizer = cv2.face.createLBPHFaceRecognizer()
    # face_recognizer = cv2.face_LBPHFaceRecognizer.create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_cascade = cv2.CascadeClassifier('D:/SecurityCam Final/SecurityCam/face/haarcascade_frontalface_default.xml')

    faces = []
    labels = []
    label_map = {}
    current_label = 0
    
    print("Training faces...")

    for name in sorted(os.listdir('faces')):
        person_path = os.path.join('faces', name)
        if not os.path.isdir(person_path):
            continue  
        
        label_map[current_label] = name  
        print(f"Processing {name}...")

        for image_filename in os.listdir(person_path):
            image_path = os.path.join(person_path, image_filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if image is None:
                print(f"Warning: Unable to read image {image_path}. Skipping.")
                continue

            faces_detected = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
            if len(faces_detected) == 0:
                print(f"No face detected in image {image_path}. Skipping.")
                continue
            
            (x, y, w, h) = faces_detected[0]
            faces.append(image[y:y+h, x:x+w]) 
            labels.append(current_label)  
        
        current_label += 1
    
    if len(faces) == 0:
        print("Error: No faces found for training. Please ensure you have images captured.")
        return

    face_recognizer.train(faces, np.array(labels))

    face_recognizer.save('trained_faces.yml')
    print("Training completed. Model saved as 'trained_faces.yml'.")



def recognize_faces(request):
    # face_recognizer = cv2.face.createLBPHFaceRecognizer()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('D:/SecurityCam Final/SecurityCam/trained_faces.yml')
    
    face_cascade = cv2.CascadeClassifier('D:/SecurityCam Final/SecurityCam/face/haarcascade_frontalface_default.xml')
    
    video_capture = cv2.VideoCapture(0)

    label_map = {}
    current_label = 0

    for name in sorted(os.listdir('faces')):
        label_map[current_label] = name
        current_label += 1

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        
        for (x, y, w, h) in faces_detected:
            face_region = gray[y:y+h, x:x+w]
            label, confidence = face_recognizer.predict(face_region)
            
            print(f"Detected Label: {label}, Confidence: {confidence}")

            # Lower confidence = better match in LBPH
            if confidence > 80:  # Higher threshold for unknown (more lenient)
                name = "Unknown"
                confidence_text = f"Low confidence: {round(confidence)}"
            else:
                name = label_map.get(label, "Unknown")
                confidence_text = f"Confidence: {round(100 - confidence)}%"

            # Capture screenshot for both known and unknown faces
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f'screenshot_{name}_{timestamp}.jpg'
            screenshot_path = os.path.join('screenshots', screenshot_filename)

            # Ensure the 'screenshots' directory exists
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')

            cv2.imwrite(screenshot_path, frame)

            # Log all faces (both known and unknown)
            log_to_csv(name, screenshot_path)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"{name} {confidence_text}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            
            current_time = time.time()

            # Handle unknown faces separately
            if name == "Unknown" and (name not in last_email_time or current_time - last_email_time[name] > 60):
                # subject = "Unknown Face Detected"
                # body = f"An unknown face has been detected at {time.strftime('%Y-%m-%d %H:%M:%S')}."
                # to_email = settings.DEFAULT_RECEIVER_EMAIL
                send_email(screenshot_path, name)
                
                # Update last email sent time
                # last_email_time[name] = current_time
            if name != "Unknown" and (name not in last_email_time or current_time - last_email_time[name] > 60):
                send_email(screenshot_path, name)


        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def log_to_csv(name, screenshot_path):
    with open('face_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([name, current_time, screenshot_path])


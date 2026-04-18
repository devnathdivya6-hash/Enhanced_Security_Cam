import os
import numpy as np
import cv2
import tensorflow as tf
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import preprocess_input
import pandas as pd
from .models import UploadedVideo
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

# Load the trained LSTM model
MODEL_PATH = "D:/SecurityCam Final/SecurityCam/violence_detection/data/violence_vedio_model.h5"

# Load VGG16 for feature extraction
base_model = VGG16(weights="imagenet", include_top=True)
transfer_layer = base_model.get_layer("fc2")
image_model_transfer = Model(inputs=base_model.input, outputs=transfer_layer.output)

def get_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    for _ in range(20):
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224))
        frame = preprocess_input(frame)  # Apply VGG16 preprocessing
        frames.append(frame)

    cap.release()

    if len(frames) < 20:
        while len(frames) < 20:
            frames.append(frames[-1])  # Pad with last frame

    frames = np.array(frames)
    return image_model_transfer.predict(frames)

# Video upload view
def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        uploaded_video = UploadedVideo.objects.create(video=filename)
        return redirect('violence_result', video_id=uploaded_video.id)
    return render(request, 'upload.html')

# Video processing and result display
def violence_result(request, video_id):
    uploaded_video = UploadedVideo.objects.get(id=video_id)
    video_path = uploaded_video.video.path
    
    # Extract processed frames (VGG16 features)
    frames = get_frames(video_path)
    frames = np.expand_dims(frames, axis=0)  # Reshape for LSTM input (1, 20, 4096)
    
    # Run prediction
    prediction = model.predict(frames)
    print(prediction)
    classes = ["Violence", "No Violence"]
    predicted_class = classes[np.argmax(prediction)]

    if predicted_class == "Violence":
        send_illegal_detection_email(video_path)
    
    # Create result dataframe
    df_res = pd.DataFrame([[prediction[0][1], prediction[0][0], predicted_class]],
                           columns=['No Violence', 'Violence', 'Prediction'])
    
    return render(request, 'violence_result.html', {'video': uploaded_video, 'prediction': predicted_class, 'df_res': df_res.to_html()})

# Function to send an email with video and frame attachment
def send_illegal_detection_email(video_path):
    subject = 'Violence Detection Alert'
    message = 'Violence detected in the camera. Attached is the evidence.'
    
    # Extract a frame from the video and save it as an image
    frame_path = extract_frame(video_path)
    
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.DEFAULT_RECEIVER_EMAIL]
    )
    
    # Attach the frame image
    if frame_path:
        email.attach_file(frame_path)
    
    # Attach the full video
    if os.path.exists(video_path):
        email.attach_file(video_path)
    
    # Send the email
    email.send()
    
    # Clean up: Remove the extracted frame after sending
    if frame_path:
        os.remove(frame_path)

def extract_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()
    
    if success:
        frame_path = os.path.join(settings.MEDIA_ROOT, 'violence_frame.jpg')
        cv2.imwrite(frame_path, frame)
        return frame_path
    return None






















# import os
# import numpy as np
# import cv2
# import tensorflow as tf
# from django.shortcuts import render, redirect
# from django.core.files.storage import FileSystemStorage
# from tensorflow.keras.models import load_model
# from tensorflow.keras.applications import VGG16
# from tensorflow.keras.models import Model
# from tensorflow.keras.applications.vgg16 import preprocess_input
# import pandas as pd
# from .models import UploadedVideo
# from django.core.mail import send_mail
# from django.conf import settings

# # Load the trained LSTM model
# MODEL_PATH = "C:/Users/User/Desktop/Enhanced Security/virtual_env/SecurityCam/violence_detection/data/violence_vedio_model.h5"
# model = load_model(MODEL_PATH)

# # Load VGG16 for feature extraction
# base_model = VGG16(weights="imagenet", include_top=True)
# transfer_layer = base_model.get_layer("fc2")
# image_model_transfer = Model(inputs=base_model.input, outputs=transfer_layer.output)


# def get_frames(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frames = []

#     for _ in range(20):
#         success, frame = cap.read()
#         if not success:
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame = cv2.resize(frame, (224, 224))
#         frame = preprocess_input(frame)  # Apply VGG16 preprocessing
#         frames.append(frame)

#     cap.release()

#     if len(frames) < 20:
#         while len(frames) < 20:
#             frames.append(frames[-1])  # Pad with last frame

#     frames = np.array(frames)
#     return image_model_transfer.predict(frames)


# # Video upload view
# def upload_video(request):
#     if request.method == 'POST' and request.FILES['video']:
#         video = request.FILES['video']
#         fs = FileSystemStorage()
#         filename = fs.save(video.name, video)
#         uploaded_video = UploadedVideo.objects.create(video=filename)
#         return redirect('violence_result', video_id=uploaded_video.id)
#     return render(request, 'upload.html')

# # Video processing and result display
# def violence_result(request, video_id):
#     uploaded_video = UploadedVideo.objects.get(id=video_id)
#     video_path = uploaded_video.video.path
    
#     # Extract processed frames (VGG16 features)
#     frames = get_frames(video_path)
#     frames = np.expand_dims(frames, axis=0)  # Reshape for LSTM input (1, 20, 4096)
    
#     # Run prediction
#     prediction = model.predict(frames)
#     print(prediction)
#     classes = ["Violence", "No Violence"]
#     predicted_class = classes[np.argmax(prediction)]

#     if predicted_class == "Violence":
#         send_illegal_detection_email()
    
#     # Create result dataframe
#     df_res = pd.DataFrame([[prediction[0][1], prediction[0][0], predicted_class]],
#                            columns=['No Violence', 'Violence', 'Prediction'])
    
#     return render(request, 'violence_result.html', {'video': uploaded_video, 'prediction': predicted_class, 'df_res': df_res.to_html()})


# # def violence_result(request, video_id):
# #     uploaded_video = UploadedVideo.objects.get(id=video_id)
# #     video_path = uploaded_video.video.path
    
# #     # Extract processed frames (VGG16 features)
# #     frames = get_frames(video_path)
# #     frames = np.expand_dims(frames, axis=0)  # Reshape for LSTM input (1, 20, 4096)
    
# #     # Run prediction
# #     prediction = model.predict(frames)
# #     print("Prediction: ", prediction)
    
# #     # Define the class names
# #     classes = ["Violence", "No Violence"]
    
# #     # Find predicted class and confidence
# #     predicted_class = classes[np.argmax(prediction)]
# #     confidence = np.max(prediction)  # The confidence of the prediction
    
# #     # Set a threshold for confidence to detect violence
# #     confidence_threshold = 0.1  # Set this to an appropriate value based on model behavior
    
# #     # Only consider the video as "Violence" if the confidence exceeds the threshold
# #     if predicted_class == "Violence" and confidence > confidence_threshold:
# #         send_illegal_detection_email()

# #     # Create result dataframe
# #     df_res = pd.DataFrame([[prediction[0][1], prediction[0][0], predicted_class, confidence]],
# #                            columns=['No Violence', 'Violence', 'Prediction', 'Confidence'])
    
# #     return render(request, 'violence_result.html', {'video': uploaded_video, 'prediction': predicted_class, 'df_res': df_res.to_html()})


# def send_illegal_detection_email():
#     subject = 'Violence Detection Alert'
#     message = f"Volence detected in the camera"
#     send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.DEFAULT_RECEIVER_EMAIL])

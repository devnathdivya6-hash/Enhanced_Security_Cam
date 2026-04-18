import os
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Detection
from gtts import gTTS
from .utils import label_map_util, visualization_utils as viz_utils


# Predefined list of illegal objects (customize this list as needed)
ILLEGAL_OBJECTS = ['gun', 'knife', 'bomb', 'weapon']  # Add more illegal objects if needed

def detect(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Create the 'uploads' directory if it doesn't exist
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Save the uploaded image
        image_path = os.path.join(uploads_dir, uploaded_file.name)
        with open(image_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Load the TensorFlow object detection model
        detect_fn = tf.saved_model.load("D:/SecurityCam Final/SecurityCam/object/saved_model")
        PATH_TO_LABELS = "D:/SecurityCam Final/SecurityCam/object/data/mscoco_label_map.pbtxt"
        category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

        # Load image into numpy array
        image_np = np.array(Image.open(image_path))
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run the model on the image
        detections = detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        # Visualize the results on the image
        image_np_with_detections = image_np.copy()

        # Capture the full return result
        result = viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'], 
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.6,
            agnostic_mode=False)

        # Get the class indices
        detected_classes = detections['detection_classes'].astype(int)
        detected_objects = [category_index.get(cls, {}).get('name', 'Unknown') for cls in detected_classes]

        # Find the illegal objects detected
        illegal_detected_objects = [obj for obj in detected_objects if obj in ILLEGAL_OBJECTS]

        # Create the 'output' directory if it doesn't exist
        output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the processed image
        output_image_path = os.path.join(output_dir, uploaded_file.name)
        cv2.imwrite(output_image_path, cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))

        # Save the detection result in the database (save all detected objects)
        detection = Detection.objects.create(
            user=request.user,
            image=uploaded_file,
            result=", ".join(detected_objects),  # Save all detected objects
            output_image=output_image_path
        )

        # If illegal objects are detected, send an email
        if illegal_detected_objects:
            send_illegal_detection_email(illegal_detected_objects, uploaded_file.name)

        # Pass detected illegal objects to the template
        return render(request, 'detect_object.html', {
            'data': uploaded_file.name,
            'illegal_detected_objects': illegal_detected_objects,
            'detection': detection
        })

    return render(request, 'detect_object.html')


def send_illegal_detection_email(illegal_detected_objects, image_name):
    subject = 'Illegal Object Detection Alert'
    message = f"The following illegal objects were detected: {', '.join(illegal_detected_objects)}\n\nImage: {image_name}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.DEFAULT_RECEIVER_EMAIL])


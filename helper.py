import os
import streamlit as st
import cv2
from ultralytics import YOLO
import supervision as sv
from SafetyEquipmentDetection.pipeline.training_pipeline import TrainPipeline
from SafetyEquipmentDetection.utils.main_utils import decodeImage, encodeImageIntoBase64



# Define paths
MODEL_PATH = "./best.pt"
#MODEL_PATH = "artifacts/model_trainer/best.pt"
IMAGE_PATH = "inputImage.jpeg"

# Define live frame size
FRAME_WIDTH = 640
FRAME_HEIGHT = 600

# Create an instance of the TrainPipeline class
pipeline = TrainPipeline()

def clear_run_folder():
    # Remove the 'runs' directory if it exists
    if os.path.exists("runs"):
        os.system("rm -rf runs")

def train_model():
    try:
        with st.spinner("Processing..."):
            pipeline.run_pipeline()
            st.success("Training Successful!!")
    except Exception as e:
        st.error(f"An error occurred during training: {str(e)}")


def predict_image(image_data):
    try:
        st.write("Running prediction...")
        decodeImage(image_data, IMAGE_PATH)

        # Verify the saved image
        image_path = os.path.abspath(f"./data/{IMAGE_PATH}")

        # Run YOLO prediction
        command = f"yolo task=detect mode=predict model={MODEL_PATH} conf=0.2 source={image_path} save=True"
        os.system(command)

        # Check if the output directory exists
        output_dir = "runs/detect/predict/"
        if not os.path.exists(output_dir):
            st.error(f"Prediction output directory does not exist: {output_dir}")
            return None

        # Verify that the expected file exists
        output_image_path = os.path.join(output_dir, "inputImage.jpeg")
        if not os.path.exists(output_image_path):
            st.error(f"Predicted image not found: {output_image_path}")
            return None

        # Convert the output image to base64
        opencodedbase64 = encodeImageIntoBase64(output_image_path)
        clear_run_folder()

        return opencodedbase64.decode('utf-8')

    except Exception as e:
        st.error(f"An error occurred during prediction: {str(e)}")
        return None
    

def live_detection():
    # Initialize YOLO model
    model = YOLO(MODEL_PATH)

    # Initialize BoxAnnotator for drawing bounding boxes
    BOX_ANNOTATOR = sv.BoxAnnotator(thickness=2)
    LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=0.5, text_color=sv.Color.BLACK)

    # Start the video capture from the system's camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # Placeholder for displaying video frames in Streamlit
    stframe = st.empty()

    # Create a button to stop the live detection
    stop_button = st.button("Stop Live Detection")

    while True:
        # Check if the stop button was pressed
        if stop_button:
            st.write("Stopping live detection...")
            break
        
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image from camera")
            break

        # Run the YOLO model on the captured frame
        #agnostic_nms: class-agnostic non-max suppression to filter out overlapping bounding boxes
        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_ultralytics(result)
        
        labels = [
            f"{class_name} {confidence:.2f}"
            for class_name, confidence
            in zip(detections['class_name'], detections.confidence)
        ]

        # Annotate the frame with bounding boxes and labels
        annotated_frame = BOX_ANNOTATOR.annotate(scene=frame, detections=detections)
        annotated_frame = LABEL_ANNOTATOR.annotate(annotated_frame, detections, labels=labels)

        # Display the frame in Streamlit
        stframe.image(annotated_frame, channels="BGR")
        
    # Release the video capture object
    cap.release()
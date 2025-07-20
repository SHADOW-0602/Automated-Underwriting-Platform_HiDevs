from ultralytics import YOLO
from PIL import Image
import json
import os

# Singleton for caching YOLO model
class YOLOModel:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YOLOModel, cls).__new__(cls)
            try:
                cls._model = YOLO('yolov8n.pt')  # Load model once
            except Exception as e:
                raise RuntimeError(f"Failed to load YOLO model: {str(e)}")
        return cls._instance

    @property
    def model(self):
        return self._model

# Load configuration
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    POTENTIAL_RISK_OBJECTS = config['potential_risk_objects']
except FileNotFoundError:
    raise FileNotFoundError("config.json not found. Please ensure it exists in the project directory.")
except json.JSONDecodeError:
    raise ValueError("Invalid config.json format. Please check the JSON syntax.")

def analyze_property_images(image_files):
    """
    Analyzes a list of images to detect objects using YOLOv8.

    Args:
        image_files: A list of uploaded image files from Streamlit.

    Returns:
        A dictionary summarizing detected objects, focusing on potential risks.

    Raises:
        ValueError: If image_files is empty or contains unsupported formats.
        RuntimeError: If image processing fails.
    """
    if not image_files:
        raise ValueError("No images provided for analysis.")
    
    # Validate image formats
    supported_formats = {'png', 'jpg', 'jpeg'}
    for img in image_files:
        if img.type.split('/')[-1].lower() not in supported_formats:
            raise ValueError(f"Unsupported image format: {img.type}. Supported formats: {supported_formats}")

    detected_objects = []
    risk_tags = []
    model = YOLOModel().model

    for image_file in image_files:
        try:
            # Open the image file
            img = Image.open(image_file)
            
            # Perform object detection
            results = model(img)

            # Process results
            for r in results:
                for box in r.boxes:
                    # Get the class name
                    class_name = model.names[int(box.cls)]
                    detected_objects.append(class_name)
                    
                    # Check if the detected object is in our potential risk list
                    if class_name in POTENTIAL_RISK_OBJECTS:
                        risk_tags.append(class_name)
        except Exception as e:
            raise RuntimeError(f"Failed to process image {image_file.name}: {str(e)}")

    analysis_result = {
        "all_detected_objects": list(set(detected_objects)),
        "risk_tags": list(set(risk_tags))
    }
    
    return analysis_result

if __name__ == '__main__':
    try:
        with open('samples/property.jpg', 'rb') as f:
            analysis = analyze_property_images([f])
            print("--- Image Analysis ---")
            print(analysis)
    except FileNotFoundError:
        print("Create a sample 'samples/property.jpg' to test the image analyzer.")
    except Exception as e:
        print(f"Error during test: {str(e)}")
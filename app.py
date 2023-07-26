import cv2
import os
import base64
from flask import Flask, request, render_template

app = Flask(__name__)

def convert_image(image_path, format):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale if the desired format is "grayscale"
    if format.lower() == "grayscale":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, buffer = cv2.imencode('.jpg', gray_image)
    else:
        # Convert the image to the desired format using OpenCV
        _, buffer = cv2.imencode('.' + format, image)

    # Encode the converted image to base64 for display and download
    converted_image = base64.b64encode(buffer).decode('utf-8')
    return converted_image

def invert_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Invert the colors of the image using OpenCV
    inverted_image = cv2.bitwise_not(image)

    # Encode the inverted image to base64 for display and download
    _, buffer = cv2.imencode('.jpg', inverted_image)
    converted_image = base64.b64encode(buffer).decode('utf-8')
    return converted_image

def detect_edges(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Detect edges in the image using Canny edge detection
    edges = cv2.Canny(image, 100, 200)

    # Encode the edges image to base64 for display and download
    _, buffer = cv2.imencode('.jpg', edges)
    converted_image = base64.b64encode(buffer).decode('utf-8')
    return converted_image

def insert_text(image_path, text):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Define the font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    # Add the text to the image
    cv2.putText(image, text, (50, 50), font, font_scale, (0, 0, 255), font_thickness)

    # Encode the image with the text to base64 for display and download
    _, buffer = cv2.imencode('.jpg', image)
    converted_image = base64.b64encode(buffer).decode('utf-8')
    return converted_image

def blur_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Apply Gaussian blur to the image
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Encode the blurred image to base64 for display and download
    _, buffer = cv2.imencode('.jpg', blurred_image)
    converted_image = base64.b64encode(buffer).decode('utf-8')
    return converted_image
    
@app.route('/convert_image', methods=['POST'])
def convert_image_route():
    # Get the uploaded image file
    image_file = request.files['image_file']
    
    # Save the uploaded image to a temporary file
    image_path = os.path.join('static', 'uploaded_image.jpg')
    image_file.save(image_path)

    # Get the desired format from the text box
    format = request.form.get('format', '').strip()

    # Convert the image based on the user's input
    if format.lower() == "grayscale":
        converted_image = convert_image(image_path, format)
    elif format.lower() == "invert":
        converted_image = invert_image(image_path)
    elif format.lower() == "detect edges":
        converted_image = detect_edges(image_path)
    elif format.lower().startswith("insert text"):
        # Extract the text from the input
        text = format[len("insert text:"):].strip()
        converted_image = insert_text(image_path, text)
    else:
        # If the format is not recognized, return the original image
        _, buffer = cv2.imencode('.jpg', cv2.imread(image_path))
        converted_image = base64.b64encode(buffer).decode('utf-8')

    # Delete the temporary uploaded image file
    os.remove(image_path)

    # Return the converted image to the HTML template for display and download
    return render_template('index.html', converted_image=f"data:image/jpeg;base64,{converted_image}")

@app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, Response  # Import the Flask class from the flask library, the render_template function is used to render the HTML template, and the Response class is used to generate the response object
from picamera2 import Picamera2 # Import Picamera2 class from picamera2 library for accessing and controlling the camera 
import time # Import time module, which can be used to handle time-related tasks 
import cv2 # Import OpenCV library for image processing

app = Flask(__name__) # Create an instance of the Flask application

def gen_frames(): # Define a generator function that generates the image captured by the camera on a frame-by-frame basis 
    picam2 = Picamera2() # Create an instance of Picamera2

    # Configure camera parameters and set the format and size of the video 
    picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))

    picam2.start() # Start the camera 
    while True: 
        frame = picam2.capture_array() # Capture a frame from the camera 
        frame = cv2.cvtColor(frame, cv2. COLOR_BGR2RGB) 
        ret, buffer = cv2.imencode('.jpg', frame) # Encodes the captured image frame to JPEG format

        frame = buffer.tobytes() # Convert JPEG images to byte streams

        # Use yield to return an image byte stream, so that you can send video frames continuously to form a video stream 
        yield (b'--frame\r\n' 
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/') # Define the root route 
def index(): 
    return render_template('index.html') # Return index.html page

@app.route('/video_feed') # Define the video stream route 
def video_feed(): 
    # Returns the response object, the content is the video stream, and the content type is multipart/x-mixed-replace 
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True) # Start the Flask application, listen on port 5000 on all network interfaces, and enable debug mode
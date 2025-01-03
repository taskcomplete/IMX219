from flask import Flask, Response
import cv2

app = Flask(__name__)

# Використання libcamera через GStreamer
camera = cv2.VideoCapture('libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
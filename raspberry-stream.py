from flask import Flask, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Захоплення кадру з камери
        success, frame = camera.read()
        if not success:
            break
        else:
            # Кодування кадру в JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        # Повернення кадру як HTTP-відповідь
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Маршрут для трансляції відео
@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Тестова сторінка
@app.route('/test')
def test_page():
    return "Hello, this is a test page for Raspberry Pi video streaming."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
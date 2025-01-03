from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30

picam2.start()
time.sleep(5)
picam2.capture_file("test.jpg")
picam2.stop()
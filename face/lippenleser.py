import cv2
import dlib
import numpy as np
import time
from colorama import init, Fore, Style

init()  # Initialize colorama

def resize_frame(frame, new_width=200):
    height, width = frame.shape[:2]
    # a = width / new_width
    # new_height = int(height / a)
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame

def frame_to_ascii(frame):
    ascii_chars = "@%/\#*+=_-:. "
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{"+"}[]?-_+~<>i!lI;:,\"^`'. "
    ascii_chars = gscale1
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pixels = np.array(gray_frame)
    ascii_str = ""
    for row in pixels:
        ascii_str += "\n"
        for pixel in row:
            ascii_str += ascii_chars[pixel // 32]
    return ascii_str

def get_lips_landmarks(shape):
    lips_points = []
    for i in range(48, 60):
        lips_points.append((shape.part(i).x, shape.part(i).y))
    return lips_points

def webcam_to_ascii():
    capture = cv2.VideoCapture(0)  # 0 for default webcam, or use the webcam index if multiple webcams are available

    # Initialize dlib's face detector and shape predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    file_name = "ascii_art.txt"
    with open(file_name, "w") as f:
        with open(file_name+"2.txt", "w") as r:
            while True:
                ret, frame = capture.read()
                if not ret:
                    break

                resized_frame = resize_frame(frame)

                # Convert the resized frame to grayscale
                gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the grayscale frame
                faces = detector(gray_frame)

                # Iterate over detected faces
                for face in faces:
                    # Predict facial landmarks for the face
                    landmarks = predictor(gray_frame, face)

                    # Get the landmarks for the lips
                    lips_landmarks = get_lips_landmarks(landmarks)
                    f.write(str(lips_landmarks))

                    # Convert the lips landmarks to NumPy array
                    lips_array = np.array(lips_landmarks)

                    # Draw the lips on the resized frame
                    cv2.polylines(resized_frame, [lips_array], True, (0, 255, 0), 1)

                # Convert the frame to ASCII art
                ascii_str = frame_to_ascii(resized_frame)
                r.write(str(ascii_str))

                # Print the ASCII art
                print(f"{Fore.GREEN}{ascii_str}{Style.RESET_ALL}")

                if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
                    break

        capture.release()
        cv2.destroyAllWindows()

# Start the webcam to ASCII conversion
webcam_to_ascii()

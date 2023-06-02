# import cv2
# import numpy as np

# def resize_frame(frame, new_width=100):
#     height, width = frame.shape[:2]
#     ratio = height / width / 1.65
#     new_height = int(new_width * ratio)
#     resized_frame = cv2.resize(frame, (new_width, new_height))
#     return resized_frame

# def frame_to_ascii(frame):
#     ascii_chars = "@%#*+=-:. "
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     pixels = np.array(gray_frame)
#     ascii_str = ""
#     for row in pixels:
#         ascii_str += "\n"
#         for pixel in row:
#             ascii_str += ascii_chars[pixel // 32]
#     return ascii_str

# def webcam_to_ascii():
#     capture = cv2.VideoCapture(0)  # 0 for default webcam, or use the webcam index if multiple webcams are available

#     while True:
#         ret, frame = capture.read()
#         if not ret:
#             break

#         resized_frame = resize_frame(frame)
#         ascii_str = frame_to_ascii(resized_frame)
#         print(ascii_str)

#         if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
#             break

#     capture.release()
#     cv2.destroyAllWindows()

# # Start the webcam to ASCII conversion
# webcam_to_ascii()
# import cv2
# import numpy as np
# import os

# def resize_frame(frame, new_width=200):
#     height, width = frame.shape[:2]
#     ratio = height / width / 1.65
#     new_height = int(new_width * ratio)
#     resized_frame = cv2.resize(frame, (new_width, new_height))
#     return resized_frame

# def frame_to_ascii(frame):
#     ascii_chars = "@%#*+=_-:. "
#     # num_chars = len(ascii_chars)
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     pixels = np.array(gray_frame)
#     ascii_str = ""
#     for row in pixels:
#         ascii_str += "\n"
#         for pixel in row:
#             ascii_str += ascii_chars[pixel // (28)]
#             # ascii_str += ascii_chars[pixel // (256 // num_chars)]
#     return ascii_str

# clear = lambda: os.system('cls')
# def webcam_to_ascii():
#     capture = cv2.VideoCapture(0)  # 0 for default webcam, or use the webcam index if multiple webcams are available

#     while True:
#         ret, frame = capture.read()
#         if not ret:
#             break

#         resized_frame = resize_frame(frame,100)
#         ascii_str = frame_to_ascii(resized_frame)
#         # clear()
#         print(ascii_str)

#         if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
#             break

#     capture.release()
#     cv2.destroyAllWindows()

# # Start the webcam to ASCII conversion
# webcam_to_ascii()
import cv2
import numpy as np
import time
def resize_frame(frame, new_width=200):
    height, width = frame.shape[:2]
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame

def frame_to_ascii(frame):
    ascii_chars = "@%/\#*+=_-:. "
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pixels = np.array(gray_frame)
    ascii_str = ""
    # ascii_str1 = ""
    for row in pixels:
        ascii_str += "\n"
        # ascii_str1 += "\n"
        for pixel in row:
            ascii_str += ascii_chars[pixel // 32]
            # ascii_str += "___________________________\n"
        ascii_str += ascii_chars[pixel // 28]
    # print(ascii_str1)
    time.sleep(0.05)
    return ascii_str

def webcam_to_ascii():
    capture = cv2.VideoCapture(0)  # 0 for default webcam, or use the webcam index if multiple webcams are available

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        resized_frame = resize_frame(frame)
        ascii_str = frame_to_ascii(resized_frame)
        print(ascii_str)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break

    capture.release()
    cv2.destroyAllWindows()

# Start the webcam to ASCII conversion
webcam_to_ascii()

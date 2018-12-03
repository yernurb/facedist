import cv2
import dlib
from imutils.video import VideoStream
import imutils
import time


camera = VideoStream(src=0).start()
detector = dlib.get_frontal_face_detector()
reduced_frame_counter = 0
face_box = dlib.rectangle(0,0,0,0)
face_area = 0
time.sleep(2)

def getNormalFrame():
    return imutils.resize(camera.read(), width=800)

def getReducedFrame():
    return imutils.resize(camera.read(), width=400)

def getMaxFace():
    reduced_frame = getReducedFrame()
    faces = detector(reduced_frame, 0)
    max_area = 0
    max_face = dlib.rectangle(0,0,0,0)
    if len(faces) == 0:
        return max_face, 0
    for face in faces:
        area = face.area()
        if area > max_area:
            max_area = face.area()
            max_face = face
    return max_face, max_area
        

while(True):
    frame = getNormalFrame()
    if reduced_frame_counter < 0:
        face_box, face_area = getMaxFace()
        reduced_frame_counter = 10
    text = ""
    if face_area > 0:
        text = "Area: " + str(face_area)
        pt1 = (2*face_box.left(), 2*face_box.top())
        pt2 = (2*face_box.right(), 2*face_box.bottom())
        cv2.rectangle(frame, pt1, pt2, (0,0,255), 2)
    else:
        text = "No face found"

    cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Frame", frame)

    reduced_frame_counter -= 1
    key = cv2.waitKey(1) & 0xFF    
    if key == ord("q"):
        break

cv2.destroyAllWindows()
camera.stop()

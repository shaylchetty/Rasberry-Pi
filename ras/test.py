import requests
import cv2
import mediapipe as mp
import helper

# Constants
RASPBERRY_PI_IP = "192.168.5.9"
RASPBERRY_PI_PORT = 8000


def track_human_motion():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    face_top = frame_height

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for x, y, w, h in faces:
            face_top = int(y - (0.25 * h))

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            send_signal_to_raspberry_pi()

            landmarks = results.pose_landmarks.landmark
            coordinates = [(int(landmark.x * frame_width), int(landmark.y * frame_height)) for landmark in landmarks]

            top_left_corner, bottom_right_corner = helper.closest_coordinates(
                coordinates, frame_width, frame_height
            )

            if top_left_corner[1] > face_top:
                top_left_corner = (
                    top_left_corner[0],
                    face_top,
                )

            if coordinates:
                center_point = (
                    sum(x for x, y in coordinates) // len(coordinates),
                    sum(y for x, y in coordinates) // len(coordinates),
                )

            image_with_landmarks = frame.copy()
            cv2.circle(image_with_landmarks, center_point, 10, (0, 255, 0), -1)
            cv2.imshow("Motion Tracking", image_with_landmarks)
        else:
            off_signal_to_raspberry_pi()
            cv2.imshow("Motion Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def send_signal_to_raspberry_pi():
    send_signal("motion-detected")


def off_signal_to_raspberry_pi():
    send_signal("motion-not-detected")


def send_signal(action):
    try:
        response = requests.post(f"http://{RASPBERRY_PI_IP}:{RASPBERRY_PI_PORT}/{action}")
        if response.status_code == 200:
            print("Signal sent successfully")
    except requests.exceptions.RequestException as e:
        print("Error sending signal:", e)


if __name__ == "__main__":
    track_human_motion()

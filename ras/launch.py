import requests
import cv2
import mediapipe as mp

# Constants
RASPBERRY_PI_IP = "192.168.5.9"
RASPBERRY_PI_PORT = 8000


def track_human_motion():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit the loop if reading from webcam fails

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            right_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            head_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

            if right_wrist_landmark.y < head_landmark.y or left_wrist_landmark.y < head_landmark.y:
                text = "Release"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 4, 2)[0]
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = text_size[1] + 50
                cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
                send_signal_to_raspberry_pi()
            else:
                # off_signal_to_raspberry_pi()
                pass

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Full Body Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def send_signal_to_raspberry_pi():
    send_signal("motion-detected")


# def off_signal_to_raspberry_pi():
#     send_signal("motion-not-detected")


def send_signal(action):
    try:
        response = requests.post(f"http://{RASPBERRY_PI_IP}:{RASPBERRY_PI_PORT}/{action}")
        if response.status_code == 200:
            print("Signal sent successfully")
    except requests.exceptions.RequestException as e:
        print("Error sending signal:", e)


if __name__ == "__main__":
    track_human_motion()

import cv2
import mediapipe as mp
import pygame

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# -----------------------------
# Load Hand Model
# -----------------------------

model_path = "models/hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)


# -----------------------------
# Music Setup
# -----------------------------

pygame.init()

pygame.mixer.music.load("songs/song1.mp3")

playing = False
started = False


# -----------------------------
# Camera Start
# -----------------------------

cap = cv2.VideoCapture(0)


while True:

    success, frame = cap.read()

    if not success:
        break


    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )


    result = detector.detect(mp_image)


    if result.hand_landmarks:

        for hand in result.hand_landmarks:


            # Draw landmarks
            for landmark in hand:

                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0,255,0),
                    -1
                )


            # -----------------------------
            # Finger Detection
            # -----------------------------

            fingers = []

            tips = [8, 12, 16, 20]

            for tip in tips:

                if hand[tip].y < hand[tip-2].y:
                    fingers.append(1)

                else:
                    fingers.append(0)


            total_fingers = sum(fingers)


            # -----------------------------
            # PLAY / RESUME
            # -----------------------------

            if total_fingers == 4:

                cv2.putText(
                    frame,
                    "PLAY",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )


                if not started:

                    pygame.mixer.music.play()

                    started = True
                    playing = True


                elif not playing:

                    pygame.mixer.music.unpause()

                    playing = True



            # -----------------------------
            # PAUSE
            # -----------------------------

            elif total_fingers == 0:

                cv2.putText(
                    frame,
                    "PAUSE",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2
                )


                if playing:

                    pygame.mixer.music.pause()

                    playing = False



    cv2.imshow(
        "AirSymphony Hand Control",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



cap.release()

pygame.mixer.music.stop()

cv2.destroyAllWindows()
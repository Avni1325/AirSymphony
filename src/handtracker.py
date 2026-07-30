import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(
        self,
        model_path="models/hand_landmarker.task",
        max_hands=2
    ):

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )


        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands
        )


        self.detector = vision.HandLandmarker.create_from_options(
            options
        )



    def find_hands(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )


        result = self.detector.detect(
            mp_image
        )


        hands = []


        if result.hand_landmarks:


            for i, landmarks in enumerate(result.hand_landmarks):


                hand_data = {

                    "landmarks": landmarks,

                    "label": result.handedness[i][0].category_name

                }


                hands.append(
                    hand_data
                )


        return hands




    def draw_landmarks(self, frame, hands):


        for hand in hands:


            for landmark in hand["landmarks"]:


                x = int(
                    landmark.x * frame.shape[1]
                )


                y = int(
                    landmark.y * frame.shape[0]
                )


                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 0),
                    -1
                )


        return frame
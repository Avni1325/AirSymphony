import cv2
import math
import time


class IntroScreen:

    def __init__(self):

        self.time = 0
        self.started = False

        self.button_x1 = 0
        self.button_y1 = 0
        self.button_x2 = 0
        self.button_y2 = 0



    def check_click(self, x, y):

        if (
            self.button_x1 < x < self.button_x2
            and
            self.button_y1 < y < self.button_y2
        ):

            self.started = True



    def draw(self, frame):

        h, w, _ = frame.shape


        self.time += 0.05



        # Animated background glow

        glow = int(
            30 + math.sin(self.time)*20
        )


        overlay = frame.copy()


        cv2.circle(
            overlay,
            (w//2, h//2),
            250,
            (glow,80,40),
            -1
        )


        frame = cv2.addWeighted(
            overlay,
            0.35,
            frame,
            0.65,
            0
        )



        # Title

        title = "AIRSYMPHONY"


        cv2.putText(
            frame,
            title,
            (w//2-170,90),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0,215,255),
            2,
            cv2.LINE_AA
        )



        cv2.putText(
            frame,
            "Music controlled by your hands",
            (w//2-145,125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (240,240,240),
            1,
            cv2.LINE_AA
        )



        # Glass instruction card

        x1 = int(w*0.12)
        x2 = int(w*0.88)

        y1 = 160
        y2 = int(h*0.68)



        card = frame.copy()


        cv2.rectangle(
            card,
            (x1,y1),
            (x2,y2),
            (40,40,45),
            -1
        )


        frame = cv2.addWeighted(
            card,
            0.75,
            frame,
            0.25,
            0
        )



        instructions = [

            "RIGHT HAND",

            "Open Palm  : Play",

            "Fist       : Pause",

            "",

            "LEFT HAND",

            "1-5 Fingers : Change Songs",

            "YO Sign    : Favourite"

        ]



        y = y1+50


        for text in instructions:


            cv2.putText(
                frame,
                text,
                (x1+35,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255,255,255),
                1,
                cv2.LINE_AA
            )


            y += 32



        # Start button

        self.button_x1 = w//2-110
        self.button_x2 = w//2+110

        self.button_y1 = h-70
        self.button_y2 = h-25



        cv2.rectangle(
            frame,
            (
                self.button_x1,
                self.button_y1
            ),
            (
                self.button_x2,
                self.button_y2
            ),
            (0,180,255),
            -1
        )



        cv2.putText(
            frame,
            "START",
            (w//2-40,h-42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,0,0),
            2,
            cv2.LINE_AA
        )



        return frame
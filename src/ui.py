import cv2
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class UI:

    def __init__(self):

        self.song_name = "No Song"

        self.lyric = ""

        self.offset = 0

        self.last_time = time.time()


        # Hindi supported font

        self.font = ImageFont.truetype(
            "C:/Windows/Fonts/Nirmala.ttf",
            24
        )



    def draw(self, frame):

        h, w, _ = frame.shape



        # -----------------------------
        # Lyrics (Top Center)
        # -----------------------------

        if self.lyric:


            img = Image.fromarray(
                cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )
            )


            draw = ImageDraw.Draw(img)



            bbox = draw.textbbox(
                (0,0),
                self.lyric,
                font=self.font
            )


            text_width = bbox[2] - bbox[0]


            x = int(
                (w - text_width) / 2
            )


            y = 25



            # Glow

            draw.text(
                (x,y),
                self.lyric,
                font=self.font,
                fill=(160,160,160)
            )


            # White text

            draw.text(
                (x,y),
                self.lyric,
                font=self.font,
                fill=(255,255,255)
            )



            frame[:] = cv2.cvtColor(
                np.array(img),
                cv2.COLOR_RGB2BGR
            )



        # -----------------------------
        # Scrolling Song Title
        # -----------------------------

        text = self.song_name



        if time.time() - self.last_time > 0.04:

            self.offset -= 1

            self.last_time = time.time()



        text_width = cv2.getTextSize(
            text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            1
        )[0][0]



        if self.offset < -(text_width + 100):

            self.offset = w



        # Black title

        cv2.putText(
            frame,
            text,
            (self.offset, h-35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0,0,0),
            1,
            cv2.LINE_AA
        )



        return frame
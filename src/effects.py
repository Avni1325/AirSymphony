import cv2
import math


class StringEffect:

    def __init__(self):

        self.time = 0



    def draw(self, frame, playing, hands):

        if not playing:

            return frame



        h, w, _ = frame.shape


        self.time += 0.08


        glow = frame.copy()



        # 4 overlapping waves

        wave_count = 4


        # closer to song title

        start_y = h - 95



        for i in range(wave_count):


            points = []


            base_y = start_y + i * 9



            for x in range(-30, w + 30, 6):


                # Different direction movement

                direction = 1 if i % 2 == 0 else -1


                wave = math.sin(
                    (x * 0.02)
                    +
                    (self.time * 2 * direction)
                    +
                    i
                ) * 12



                y = int(
                    base_y + wave
                )


                points.append(
                    (
                        x,
                        y
                    )
                )



            # Glow

            for j in range(len(points)-1):

                cv2.line(
                    glow,
                    points[j],
                    points[j+1],
                    (0,160,255),
                    9,
                    cv2.LINE_AA
                )



            # Main golden wave

            for j in range(len(points)-1):

                cv2.line(
                    frame,
                    points[j],
                    points[j+1],
                    (0,215,255),
                    2,
                    cv2.LINE_AA
                )



        # Soft glow

        frame = cv2.addWeighted(
            glow,
            0.16,
            frame,
            0.84,
            0
        )


        return frame
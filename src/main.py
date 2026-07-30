import cv2
import os

from handtracker import HandTracker
from gestures import GestureDetector
from audio import MusicController
from ui import UI
from effects import StringEffect
from lyrics import Lyrics
from intro import IntroScreen



# -----------------------------
# Setup
# -----------------------------

tracker = HandTracker(
    "models/hand_landmarker.task",
    max_hands=2
)


gesture_detector = GestureDetector()


music = MusicController(
    "songs"
)


ui = UI()

strings = StringEffect()

lyrics = Lyrics()

intro = IntroScreen()


current_song_loaded = ""



# -----------------------------
# Camera Setup
# -----------------------------

cap = cv2.VideoCapture(0)


cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)



width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)


print(
    "Camera resolution:",
    width,
    "x",
    height
)



cv2.namedWindow(
    "AirSymphony",
    cv2.WINDOW_NORMAL
)


cv2.resizeWindow(
    "AirSymphony",
    960,
    720
)



# -----------------------------
# Mouse Click
# -----------------------------
def mouse_click(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        # Convert window coordinates to camera frame coordinates

        real_x = int(x * width / 960)
        real_y = int(y * height / 720)


        intro.check_click(
            real_x,
            real_y
        )

    



cv2.setMouseCallback(
    "AirSymphony",
    mouse_click
)



# -----------------------------
# States
# -----------------------------

intro_mode = True

last_command = "NONE"



# -----------------------------
# Main Loop
# -----------------------------

while True:


    success, frame = cap.read()


    if not success:

        break



    frame = cv2.flip(
        frame,
        1
    )



    # -----------------------------
    # Intro Screen
    # -----------------------------

    if intro_mode:


        frame = intro.draw(
            frame
        )


        cv2.imshow(
            "AirSymphony",
            frame
        )


        key = cv2.waitKey(1)


        if key == 32 or intro.started:

            intro_mode = False



        if key == ord("q"):

            break



        continue



    # -----------------------------
    # Hand Tracking
    # -----------------------------

    hands = tracker.find_hands(
        frame
    )


    frame = tracker.draw_landmarks(
        frame,
        hands
    )



    if hands:


        for hand in hands:


            command = gesture_detector.get_gesture(
                hand
            )



            if command != last_command:



                if command == "PLAY":

                    music.play()



                elif command == "PAUSE":

                    music.pause()



                elif command.startswith("SONG_"):


                    number = int(
                        command.split("_")[1]
                    )


                    music.play_song(
                        number
                    )



            last_command = command



    else:

        last_command = "NONE"



    # -----------------------------
    # Lyrics
    # -----------------------------

    if music.current_song:


        filename = os.path.splitext(
            os.path.basename(
                music.current_song
            )
        )[0]



        if filename != current_song_loaded:


            lyrics.load(
                os.path.join(
                    "lyrics",
                    filename + ".lrc"
                )
            )


            current_song_loaded = filename



    if music.playing:


        ui.lyric = lyrics.get_line(
            music.get_position()
        )


    else:

        ui.lyric = ""



    # -----------------------------
    # UI Effects
    # -----------------------------

    ui.song_name = music.get_song_name()



    frame = strings.draw(
        frame,
        music.playing,
        hands
    )


    frame = ui.draw(
        frame
    )



    cv2.imshow(
        "AirSymphony",
        frame
    )



    if cv2.waitKey(1) & 0xFF == ord("q"):

        break



cap.release()

cv2.destroyAllWindows()
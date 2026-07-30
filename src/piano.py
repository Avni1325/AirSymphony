import cv2

# -----------------------------
# Piano Settings
# -----------------------------

KEYS = ["C", "D", "E", "F", "G", "A", "B", "C"]
KEY_HEIGHT = 120

# -----------------------------
# Camera
# -----------------------------

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Get actual frame size
    height, width = frame.shape[:2]

    # Width of each piano key
    key_width = width // len(KEYS)

    # -----------------------------
    # Draw Piano Keys
    # -----------------------------

    for i, key in enumerate(KEYS):

        x1 = i * key_width
        y1 = height - KEY_HEIGHT

        x2 = x1 + key_width
        y2 = height

        # White key
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            -1
        )

        # Black border
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 0, 0),
            2
        )

        # Key label
        text_size = cv2.getTextSize(
            key,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            2
        )[0]

        text_x = x1 + (key_width - text_size[0]) // 2
        text_y = y1 + 70

        cv2.putText(
            frame,
            key,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2
        )

    # -----------------------------
    # Title
    # -----------------------------

    cv2.putText(
        frame,
        "AIR SYMPHONY",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.imshow("Air Symphony", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
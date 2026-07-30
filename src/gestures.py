class GestureDetector:


    def count_fingers(self, hand):

        fingers = []


        tips = [8, 12, 16, 20]


        for tip in tips:

            if hand[tip].y < hand[tip-2].y:

                fingers.append(1)

            else:

                fingers.append(0)



        return fingers




    def thumb_open(self, hand, label):


        thumb_tip = hand[4]

        thumb_joint = hand[3]



        if label == "Left":

            return thumb_tip.x < thumb_joint.x



        elif label == "Right":

            return thumb_tip.x > thumb_joint.x



        return False




    def detect_song_number(self, hand, label):


        fingers = self.count_fingers(
            hand
        )


        count = sum(fingers)



        thumb = self.thumb_open(
            hand,
            label
        )



        # YO sign = Song 6

        if (
            thumb
            and
            fingers[0] == 1
            and
            fingers[3] == 1
            and
            fingers[1] == 0
            and
            fingers[2] == 0
        ):

            return 6




        if count == 1:

            return 1


        elif count == 2:

            return 2


        elif count == 3:

            return 3


        elif count == 4:

            return 4


        elif count == 5:

            return 5



        return None




    def get_gesture(self, hand_data):


        hand = hand_data["landmarks"]

        label = hand_data["label"]



        fingers = self.count_fingers(
            hand
        )


        count = sum(fingers)



        # MIRROR FIX:
        # Physical right hand appears as Left

        if label == "Left":


            # Physical RIGHT hand controls music

            if count == 4:

                return "PLAY"


            elif count == 0:

                return "PAUSE"




        elif label == "Right":


            # Physical LEFT hand selects songs

            song = self.detect_song_number(
                hand,
                label
            )


            if song:

                return "SONG_" + str(song)




        return "NONE"
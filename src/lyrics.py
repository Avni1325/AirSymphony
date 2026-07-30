import re


class Lyrics:


    def __init__(self):

        self.lines = []



    def load(self, filename):

        self.lines = []


        try:

            with open(filename, "r", encoding="utf-8") as file:

                for line in file:

                    match = re.match(
                        r"\[(\d+):(\d+\.\d+)\](.*)",
                        line
                    )


                    if match:

                        minute = int(match.group(1))

                        second = float(match.group(2))

                        lyric = match.group(3).strip()


                        time = minute * 60 + second


                        self.lines.append(
                            (time, lyric)
                        )


        except:

            pass




    def get_line(self, current_time):


        current = ""


        for t, lyric in self.lines:

            if current_time >= t:

                current = lyric

            else:

                break


        return current
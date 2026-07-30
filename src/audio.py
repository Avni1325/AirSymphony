import pygame # type: ignore
import os


class MusicController:

    def __init__(self, song_folder="songs"):

        pygame.mixer.init()

        self.songs = []

        for file in os.listdir(song_folder):

            if file.lower().endswith(".mp3"):

                self.songs.append(
                    os.path.join(song_folder, file)
                )

        self.songs.sort()

        # =====================================
        # Song names shown in the UI
        # =====================================

        self.song_titles = {

            "song1": "Sitaare - Arijit Singh",

            "song2": "Raabta - Arijit Singh",

            "song3": "Gehra Hua - Arijit Singh",

            "song4": "Bairan - Banjaare",

            "song5": "Raat Bhar - Arijit Singh",

            "song6": "Favorite - Isabel LaRosa"

        }

        # =====================================

        self.current_index = 0
        self.current_song = None

        self.playing = False
        self.started = False



    # ---------------------------------
    # Play / Resume
    # ---------------------------------

    def play(self):

        if not self.songs:
            return

        if not self.started:

            self.current_song = self.songs[
                self.current_index
            ]

            pygame.mixer.music.load(
                self.current_song
            )

            pygame.mixer.music.play()

            self.started = True
            self.playing = True

        elif not self.playing:

            pygame.mixer.music.unpause()

            self.playing = True



    # ---------------------------------
    # Pause
    # ---------------------------------

    def pause(self):

        if self.playing:

            pygame.mixer.music.pause()

            self.playing = False



    # ---------------------------------
    # Play Selected Song
    # ---------------------------------

    def play_song(self, number):

        if not self.songs:
            return

        index = number - 1

        if index < 0 or index >= len(self.songs):
            return

        pygame.mixer.music.stop()

        self.current_index = index

        self.current_song = self.songs[
            self.current_index
        ]

        pygame.mixer.music.load(
            self.current_song
        )

        pygame.mixer.music.play()

        self.started = True
        self.playing = True



    # ---------------------------------
    # Next Song
    # ---------------------------------

    def next_song(self):

        if not self.songs:
            return

        self.current_index += 1

        if self.current_index >= len(self.songs):

            self.current_index = 0

        self.play_song(
            self.current_index + 1
        )



    # ---------------------------------
    # Current Song Name
    # ---------------------------------

    def get_song_name(self):

        if self.current_song:

            filename = os.path.splitext(

                os.path.basename(
                    self.current_song
                )

            )[0]

            return self.song_titles.get(

                filename,

                filename

            )

        return "No Song"



    # ---------------------------------
    # Is Music Playing?
    # ---------------------------------

    def is_playing(self):

        return self.playing



    # ---------------------------------
    # Current Playback Time (for lyrics)
    # ---------------------------------

    def get_position(self):

        return pygame.mixer.music.get_pos() / 1000
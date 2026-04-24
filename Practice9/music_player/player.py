import pygame # audio engine
import os # file path handling

class MusicPlayer:
    def __init__(self, tracks):
        self.playlist = tracks # list of file paths
        self.current_index = 0 # active track pointer
        self.is_playing = False # playback state
        self.track_duration = 0 # total length in seconds

    def play(self):
        track_path = self.playlist[self.current_index] # get current file
        if not self.is_playing:
            pygame.mixer.music.load(track_path) # load file
            pygame.mixer.music.play() # start playback
            self.is_playing = True
            
            # get track length for progress bar
            temp_sound = pygame.mixer.Sound(track_path)
            self.track_duration = temp_sound.get_length()
        else:
            pygame.mixer.music.unpause() # resume playback

    def stop(self):
        pygame.mixer.music.stop() # end playback
        self.is_playing = False

    def pause(self):
        pygame.mixer.music.pause() # temporary halt

    def next_track(self):
        # loop to start if at end
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.is_playing = False
        self.play()

    def prev_track(self):
        # loop to end if at start
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.is_playing = False
        self.play()

    def get_current_name(self):
        # return filename without folder path
        return os.path.basename(self.playlist[self.current_index])

    def get_progress(self):
        if not self.is_playing or self.track_duration == 0:
            return 0
        # calculate percentage (0.0 to 1.0)
        current_pos = pygame.mixer.music.get_pos() / 1000
        return min(current_pos / self.track_duration, 1.0)
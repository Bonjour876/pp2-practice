import pygame
import os

class MusicPlayer:
    def __init__(self, tracks):
        self.playlist = tracks
        self.current_index = 0
        self.is_playing = False
        self.track_duration = 0

    def play(self):
        track_path = self.playlist[self.current_index]
        if not self.is_playing:
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True
            
            temp_sound = pygame.mixer.Sound(track_path)
            self.track_duration = temp_sound.get_length()
        else:
            pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def pause(self):
        pygame.mixer.music.pause()

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.is_playing = False
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.is_playing = False
        self.play()

    def get_current_name(self):
        return os.path.basename(self.playlist[self.current_index])

    def get_progress(self):
        if not self.is_playing or self.track_duration == 0:
            return 0
        current_pos = pygame.mixer.music.get_pos() / 1000
        return min(current_pos / self.track_duration, 1.0)
import pygame
import datetime

def get_time():
    now = datetime.datetime.now()
    sec_angle = -now.second * 6
    min_angle = -now.minute * 6
    return sec_angle, min_angle

def rotate_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect
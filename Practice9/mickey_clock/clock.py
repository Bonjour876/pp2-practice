import pygame # graphics library
import datetime # time handling

def get_time():
    now = datetime.datetime.now() # current time
    sec_angle = -now.second * 6 # seconds angle (360/60)
    min_angle = -now.minute * 6 # minutes angle (360/60)
    return sec_angle, min_angle # return angles

def rotate_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle) # rotate surface
    # fix center (prevent wobbling)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect # return image and position
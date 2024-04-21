import pygame


class Texture:

    def __init__(self, file: str):
        self.__image = pygame.image.load(file)

    def get_image(self):
        return self.__image

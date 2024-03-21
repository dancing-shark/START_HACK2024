import pygame


class VoiceOutput:
    def __init__(self):
        pass

    def play(self, file_path: str):
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.delay(100)






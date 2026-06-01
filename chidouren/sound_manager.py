
import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.initialized = False
        
        try:
            self._create_sounds()
            self.initialized = True
        except Exception as e:
            print(f"音效初始化失败: {e}")

    def _create_sounds(self):
        sample_rate = 44100
        bits = -16
        channels = 2
        buffer = 512
        
        pygame.mixer.init(sample_rate, bits, channels, buffer)

        try:
            self.sounds['dot'] = self._create_tone(440, 0.1)
            self.sounds['power_pellet'] = self._create_tone(220, 0.3)
            self.sounds['eat_ghost'] = self._create_tone(880, 0.2)
            self.sounds['death'] = self._create_tone(110, 0.5)
        except:
            pass

    def _create_tone(self, frequency, duration):
        try:
            import array
            import math
            
            sample_rate = 44100
            n_samples = int(sample_rate * duration)
            
            sound_buffer = array.array('h')
            
            for i in range(n_samples):
                t = i / sample_rate
                value = int(32767 * math.sin(2 * math.pi * frequency * t))
                sound_buffer.append(value)
                sound_buffer.append(value)
            
            sound = pygame.mixer.Sound(sound_buffer)
            return sound
        except:
            return None

    def play(self, sound_name):
        if self.initialized and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass

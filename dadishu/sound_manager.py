import pygame
import math

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except:
            pass
        self.sounds = {}
        self._init_sounds()
    
    def _init_sounds(self):
        try:
            self.sounds['mole_appear'] = self._create_tone(440, 0.1)
            self.sounds['hit'] = self._create_tone(880, 0.1)
            self.sounds['miss'] = self._create_tone(150, 0.2)
            self.sounds['level_up'] = self._create_sequence([523, 659, 784, 1047], 0.1)
            self.sounds['game_start'] = self._create_tone(523, 0.2)
            self.sounds['game_over'] = self._create_sequence([523, 440, 349, 294], 0.2)
        except:
            self.sounds = {}
    
    def _create_tone(self, frequency, duration):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        
        buf = bytearray()
        amplitude = 4096
        
        for s in range(n_samples):
            t = float(s) / sample_rate
            value = int(amplitude * math.sin(2 * math.pi * frequency * t))
            
            # 16-bit signed little endian
            buf.append(value & 0xff)
            buf.append((value >> 8) & 0xff)
            buf.append(value & 0xff)
            buf.append((value >> 8) & 0xff)
        
        sound = pygame.mixer.Sound(bytes(buf))
        sound.set_volume(0.3)
        return sound
    
    def _create_sequence(self, frequencies, duration_per_note):
        sample_rate = 22050
        buf = bytearray()
        amplitude = 4096
        
        for freq in frequencies:
            n_samples = int(sample_rate * duration_per_note)
            for s in range(n_samples):
                t = float(s) / sample_rate
                value = int(amplitude * math.sin(2 * math.pi * freq * t))
                
                buf.append(value & 0xff)
                buf.append((value >> 8) & 0xff)
                buf.append(value & 0xff)
                buf.append((value >> 8) & 0xff)
        
        sound = pygame.mixer.Sound(bytes(buf))
        sound.set_volume(0.3)
        return sound
    
    def play(self, sound_name):
        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
        except:
            pass
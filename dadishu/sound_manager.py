import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._init_sounds()
    
    def _init_sounds(self):
        self.sounds['mole_appear'] = self._create_sound(400, 0.2, 'sine')
        self.sounds['hit'] = self._create_sound(800, 0.15, 'square')
        self.sounds['miss'] = self._create_sound(200, 0.3, 'sawtooth')
        self.sounds['level_up'] = self._create_level_up_sound()
        self.sounds['game_start'] = self._create_sound(523, 0.15, 'sine')
        self.sounds['game_over'] = self._create_game_over_sound()
    
    def _create_sound(self, frequency, duration, waveform='sine'):
        sample_rate = 44100
        samples = int(sample_rate * duration)
        buffer = []
        
        for i in range(samples):
            t = i / sample_rate
            if waveform == 'sine':
                value = int(32767 * (2 * t * frequency))
            elif waveform == 'square':
                value = 32767 if (t * frequency) % 1 < 0.5 else -32767
            elif waveform == 'sawtooth':
                value = int(32767 * (2 * ((t * frequency) % 1) - 1))
            else:
                value = int(32767 * (2 * t * frequency))
            buffer.append(value)
            buffer.append(value)
        
        sound = pygame.mixer.Sound(buffer)
        sound.set_volume(0.3)
        return sound
    
    def _create_level_up_sound(self):
        notes = [523, 659, 784, 1047]
        sound = pygame.mixer.Sound(b'')
        for freq in notes:
            note_sound = self._create_sound(freq, 0.15, 'sine')
            sound = pygame.mixer.Sound(note_sound.get_raw() + sound.get_raw())
        sound.set_volume(0.3)
        return sound
    
    def _create_game_over_sound(self):
        notes = [523, 440, 349, 294]
        sound = pygame.mixer.Sound(b'')
        for freq in notes:
            note_sound = self._create_sound(freq, 0.2, 'sine')
            sound = pygame.mixer.Sound(sound.get_raw() + note_sound.get_raw())
        sound.set_volume(0.3)
        return sound
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
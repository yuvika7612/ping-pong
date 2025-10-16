import pygame
import os
import numpy as np
from pathlib import Path

class SoundManager:
    """Manages all game sound effects"""
    
    def __init__(self):
        # Initialize pygame mixer with specific settings for better quality
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        
        self.sounds = {}
        self.enabled = True
        
        # Create sounds directory if it doesn't exist
        self.sounds_dir = Path("sounds")
        self.sounds_dir.mkdir(exist_ok=True)
        
        # Generate or load sound files
        self._load_sounds()
    
    def _load_sounds(self):
        """Load sound effects from files or generate them"""
        sound_files = {
            'paddle_hit': 'paddle_hit.wav',
            'wall_bounce': 'wall_bounce.wav',
            'score': 'score.wav'
        }
        
        for sound_name, filename in sound_files.items():
            filepath = self.sounds_dir / filename
            
            # If sound file doesn't exist, generate it
            if not filepath.exists():
                print(f"Generating {filename}...")
                self._generate_sound(sound_name, filepath)
            
            # Load the sound
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(str(filepath))
                print(f"✓ Loaded {sound_name}")
            except Exception as e:
                print(f"✗ Failed to load {sound_name}: {e}")
                self.sounds[sound_name] = None
    
    def _generate_sound(self, sound_type, filepath):
        """Generate simple sound effects using numpy"""
        sample_rate = 44100
        
        if sound_type == 'paddle_hit':
            # Short, high-pitched beep (like a ping)
            duration = 0.1
            frequency = 800
            samples = self._generate_tone(frequency, duration, sample_rate)
        
        elif sound_type == 'wall_bounce':
            # Medium-pitched beep (softer than paddle)
            duration = 0.08
            frequency = 600
            samples = self._generate_tone(frequency, duration, sample_rate)
        
        elif sound_type == 'score':
            # Lower, longer beep (like a buzzer)
            duration = 0.3
            frequency = 400
            samples = self._generate_tone(frequency, duration, sample_rate, decay=True)
        
        else:
            return
        
        # Save as WAV file
        self._save_wav(samples, filepath, sample_rate)
    
    def _generate_tone(self, frequency, duration, sample_rate, decay=False):
        """Generate a sine wave tone"""
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        
        # Generate sine wave
        wave = np.sin(frequency * 2 * np.pi * t)
        
        # Apply envelope (fade in/out)
        envelope = np.ones(num_samples)
        fade_samples = int(sample_rate * 0.01)  # 10ms fade
        
        # Fade in
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        
        # Fade out or decay
        if decay:
            # Exponential decay for score sound
            envelope *= np.exp(-3 * t / duration)
        else:
            # Quick fade out
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        wave *= envelope
        
        # Convert to 16-bit integer format
        wave = (wave * 32767).astype(np.int16)
        
        return wave
    
    def _save_wav(self, samples, filepath, sample_rate):
        """Save samples as a WAV file"""
        # Convert mono to stereo
        stereo_samples = np.column_stack((samples, samples))
        
        # Create pygame Sound and save
        sound = pygame.sndarray.make_sound(stereo_samples)
        pygame.mixer.Sound.set_volume(sound, 0.5)
        
        # Save to file
        try:
            # Use scipy if available for better WAV writing
            from scipy.io import wavfile
            wavfile.write(str(filepath), sample_rate, stereo_samples)
        except ImportError:
            # Fallback: just note that file generation requires scipy
            print(f"Note: Install scipy for sound generation: pip install scipy")
    
    def play_paddle_hit(self):
        """Play paddle hit sound"""
        if self.enabled and self.sounds.get('paddle_hit'):
            self.sounds['paddle_hit'].play()
    
    def play_wall_bounce(self):
        """Play wall bounce sound"""
        if self.enabled and self.sounds.get('wall_bounce'):
            self.sounds['wall_bounce'].play()
    
    def play_score(self):
        """Play score sound"""
        if self.enabled and self.sounds.get('score'):
            self.sounds['score'].play()
    
    def toggle(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        return self.enabled
    
    def set_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(volume)
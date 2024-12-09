import librosa
import numpy as np
from pydub import AudioSegment
import soundfile as sf
import json


class AudioAnalyzer:
    def __init__(self, file_path):
        """
        Initialize the AudioAnalyzer with an audio file.
        Supports mp3, wav, and other common audio formats.
        """
        self.file_path = file_path
        self.y = None
        self.sr = None
        self.load_audio()

    def load_audio(self):
        """Load the audio file using librosa."""
        try:
            self.y, self.sr = librosa.load(self.file_path)
        except Exception as e:
            print(f"Error loading audio file: {e}")
            raise

    def get_bpm(self):
        """Extract tempo (BPM) from the audio file."""
        try:
            onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sr)
            return round(float(tempo[0]), 2)
        except Exception as e:
            print(f"Error calculating BPM: {e}")
            return None

    def get_key(self):
        """Estimate the musical key of the audio."""
        try:
            chromagram = librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
            key_labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            chroma_sum = np.sum(chromagram, axis=1)
            key_index = np.argmax(chroma_sum)
            return key_labels[key_index]
        except Exception as e:
            print(f"Error estimating key: {e}")
            return None

    def get_spectral_features(self):
        """Calculate various spectral features of the audio."""
        try:
            spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
            
            return {
                "spectral_centroid_mean": float(np.mean(spectral_centroids)),
                "spectral_rolloff_mean": float(np.mean(spectral_rolloff))
            }
        except Exception as e:
            print(f"Error calculating spectral features: {e}")
            return None

    def get_amplitude_stats(self):
        """Calculate amplitude statistics."""
        try:
            return {
                "rms_energy": float(np.sqrt(np.mean(self.y**2))),
                "peak_amplitude": float(np.max(np.abs(self.y))),
                "dynamic_range": float(np.ptp(self.y))
            }
        except Exception as e:
            print(f"Error calculating amplitude stats: {e}")
            return None

    def get_duration(self):
        """Get the duration of the audio in seconds."""
        try:
            return float(librosa.get_duration(y=self.y, sr=self.sr))
        except Exception as e:
            print(f"Error calculating duration: {e}")
            return None

    def analyze_all(self):
        """Perform complete analysis of the audio file."""
        return {
            "file_path": self.file_path,
            "duration": self.get_duration(),
            "bpm": self.get_bpm(),
            "key": self.get_key(),
            "spectral_features": self.get_spectral_features(),
            "amplitude_stats": self.get_amplitude_stats()
        }

# Example usage
def main():
    # Replace with your audio file path
    audio_file = "audio/example.mp3"
    
    try:
        analyzer = AudioAnalyzer(audio_file)
        results = analyzer.analyze_all()
        
        with open('results/results.json', 'w') as json_file:
            json.dump(results, json_file, indent=4)

    except Exception as e:
        print(f"Error analyzing audio file: {e}")
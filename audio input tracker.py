import pyaudio
import numpy as np
import scipy.fftpack

# Constants
CHUNK = 1024            # Number of audio samples per frame
FORMAT = pyaudio.paInt16 # 16-bit audio
CHANNELS = 1            # Single channel for mic input
RATE = 44100            # Sampling rate in Hz

# Initialize pyaudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

def detect_frequency(data, rate):
    # Perform FFT
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_data))
    
    # Get the magnitude of the complex numbers
    magnitudes = np.abs(fft_data)
    
    # Find the peak frequency
    peak_index = np.argmax(magnitudes)
    peak_freq = abs(freqs[peak_index] * rate)
    
    return peak_freq

# Read from mic and process the audio in real time
try:
    while True:
        # Read a chunk of audio data from the mic
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        
        # Detect the dominant frequency
        frequency = detect_frequency(data, RATE)
        
        # Print the frequency in Hz
        print(f"Detected frequency: {frequency:.2f} Hz")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()


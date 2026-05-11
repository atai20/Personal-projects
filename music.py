import numpy as np
import pyaudio


twinkle_freqs = np.random.uniform(200, 200, size=200)
twinkle_freqs2 = np.random.uniform(500, 500, size=200)


def play_sine(frequency, volume = 1, duration=10.0, twinkle_freqs = [], sample_rate=44100):
    p = pyaudio.PyAudio()
    # Generate the time array and the sine wave data
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    n = len(twinkle_freqs)

    # 1. Create indices from 0 to n-1
    # [0, 1, 2, ..., n-1]
    indexes = np.arange(n) 

    # 2. Create the high-resolution x-axis
    # It MUST start and end at the same points as 'indexes'
    x_new = np.linspace(0, n - 1, n * 1000)

    print(len(twinkle_freqs))
    frequencies = np.interp(x_new, indexes, twinkle_freqs)
    print(len(frequencies))
    print(frequencies[100])

    frequencies = np.repeat(twinkle_freqs, (duration*sample_rate)/len(twinkle_freqs))
    frequencies = np.concatenate((frequencies, np.zeros(len(t)%len(frequencies))))

    print(len(frequencies))

   

    audio_data = ((volume/100) * ((0.5 + frequencies * t)%1+0.5) * 32767).astype(np.int16)
    
    # Open a stream and play the generated data
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
    stream.write(audio_data.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_triangle(frequency, duration=1.0, sample_rate=44100):
    p = pyaudio.PyAudio()
    # Generate the time array and the sine wave data
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    frequencies = np.repeat(twinkle_freqs, (duration*sample_rate)//len(twinkle_freqs))
    

    frequencies = np.convolve(frequencies, np.ones(4)/4, mode='same')

    audio_data = (((0.5 + frequencies * t)%1+0.5) * 32767).astype(np.int16)

    
    
    # Open a stream and play the generated data
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
    stream.write(audio_data.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_square(frequency, duration=1.0, sample_rate=44100):
    p = pyaudio.PyAudio()
    # Generate the time array and the sine wave data
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Returns 32767 where the condition is True, and -32767 where False

    t = np.linspace(0, duration, int(sample_rate * duration), False)

    frequencies = np.repeat(twinkle_freqs, (duration*sample_rate)//len(twinkle_freqs))
   
    audio_data = np.where((frequencies * t) % 1 < 0.5, 32767, -32767).astype(np.int16)
    
    # Open a stream and play the generated data
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
    stream.write(audio_data.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Example: Play a 440Hz tone (A4)



play_sine(440, 100, 0.5, twinkle_freqs)

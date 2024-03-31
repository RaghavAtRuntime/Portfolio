import sounddevice as sd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame([], [], columns=['Time', 'dB'])
count = 0

def calculate_db(rms):
    return 20 * np.log10(rms)


def callback(indata, frames, time, status):
    global count
    if status:
        print(f"Error in audio input: {status}")
        return

    rms = np.sqrt(np.mean(indata ** 2))
    decibel = calculate_db(rms)
    df.loc[len(df.index)] = [float(count), abs(decibel)]
    count += 1
    # print(f"Decibel level: {decibel:.2f} dB")


# Set the sample rate and duration
sample_rate = 44100
duration = 10  # in seconds

# Start streaming audio input with the specified callback function
with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
    print("Listening for microphone input. Press Ctrl+C to exit.")
    sd.sleep(duration * 1000)  # Sleep for the specified duration

plt.plot(df['Time'], df['dB'], color='blue', alpha=0.7)
plt.xlabel('Time (s)')
plt.ylabel('Decibels (dB)')
plt.title('Scatter Plot of Time vs. Decibels')
plt.show()

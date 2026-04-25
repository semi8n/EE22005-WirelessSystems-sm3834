import serial
import matplotlib.pyplot as plt
import time

# Configuration
COM_PORT = 'COM7'
NUM_SAMPLES = 200

# Initialize an empty list to store the data
data = []

# Average function
def average_signal(data):
    if len(data) == 0:
        return None
    return sum(data) / len(data)

try:
    # Open the serial port
    with serial.Serial(COM_PORT, 115200, timeout=1) as ser:
        print(f"Connected to {COM_PORT}.")
        print(f"Logging {NUM_SAMPLES} samples...")

        # Read and log data
        while len(data) < NUM_SAMPLES:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"RAW: '{line}'")

            if line != "":
                try:
                    data.append(int(line))
                except ValueError:
                    # Ignore lines that aren't integers
                    pass

        print("Data logging complete.")

except serial.SerialException as e:
    print(f"Error: {e}")

# Calculate average
avg_rssi = average_signal(data)

if avg_rssi is not None:
    print(f"Average RSSI over {len(data)} samples: {avg_rssi:.2f} dBm")

# Plot the data
if data:
    plt.figure(figsize=(10, 6))
    plt.plot(data, label="Serial Data")

    # Plot average line
    plt.axhline(avg_rssi, linestyle='--',
                label=f"Average = {avg_rssi:.1f} dBm")

    plt.title("Serial Data Plot")
    plt.xlabel("Sample Index")
    plt.ylabel("RSSI [dBm]")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("No data collected")
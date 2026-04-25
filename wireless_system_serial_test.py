import serial
import matplotlib.pyplot as plt
import csv
import statistics

# Configuration
COM_PORT = 'COM7'
NUM_SAMPLES = 200
CSV_FILENAME = 'rssi_data.csv'

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
                    pass

        print("Data logging complete.")

except serial.SerialException as e:
    print(f"Error: {e}")

# Calculate statistics
if data:
    avg_rssi = average_signal(data)
    min_rssi = min(data)
    max_rssi = max(data)
    std_rssi = statistics.stdev(data) if len(data) > 1 else 0

    print(f"Average RSSI over {len(data)} samples: {avg_rssi:.2f} dBm")
    print(f"Minimum RSSI: {min_rssi} dBm")
    print(f"Maximum RSSI: {max_rssi} dBm")
    print(f"Standard deviation: {std_rssi:.2f} dBm")

    # Save data to CSV
    with open(CSV_FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sample Index", "RSSI (dBm)"])
        for i, value in enumerate(data, start=1):
            writer.writerow([i, value])

    print(f"Data saved to {CSV_FILENAME}")

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(data, label="RSSI Measurements")

    # Plot average line
    plt.axhline(avg_rssi, linestyle='--',
                label=f"Average = {avg_rssi:.1f} dBm")

    plt.title("RSSI Measurements from Serial Receiver")
    plt.xlabel("Sample Index")
    plt.ylabel("RSSI [dBm]")
    plt.legend()
    plt.grid()
    plt.show()

else:
    print("No data collected")

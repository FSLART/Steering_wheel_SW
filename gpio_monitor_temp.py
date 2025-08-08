#!/usr/bin/env python3
import time
from periphery import GPIO

# Initialize GPIOs
gpio11 = GPIO(11, "in")
gpio12 = GPIO(12, "in")
gpio13 = GPIO(13, "in")
gpio14 = GPIO(14, "in")

try:
    while True:
        # Read states and print (ON for pressed, OFF for not pressed)
        print(
            f"\rGPIO11: {'ON ' if gpio11.read() else 'OFF'} | "
            f"GPIO12: {'ON ' if gpio12.read() else 'OFF'} | "
            f"GPIO13: {'ON ' if gpio13.read() else 'OFF'} | "
            f"GPIO14: {'ON ' if gpio14.read() else 'OFF'}",
            end="",
        )
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram stopped")

finally:
    # Clean up
    gpio11.close()
    gpio12.close()
    gpio13.close()
    gpio14.close()
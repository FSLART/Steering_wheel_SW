#!/usr/bin/env python3
"""
GPIO Status Monitor
Shows ON/OFF status for GPIOs 11, 12, 13, 14
"""

import time
from periphery import GPIO


def monitor_gpio_status():
    try:
        # Initialize GPIOs
        gpios = {
            "OK": GPIO(11, "in"),
            "Cancel": GPIO(12, "in"),
            "Back": GPIO(13, "in"),
            "Next": GPIO(14, "in"),
        }

        print("GPIO Status Monitor")
        print("Press CTRL+C to exit")
        print("-" * 40)

        while True:
            # Move cursor to start of screen (works in most terminals)
            print("\033[H", end="")

            # Print status for each GPIO
            for name, gpio in gpios.items():
                status = "ON " if gpio.read() else "OFF"
                print(f"{name:6}: [{status}]")

            # Add some spacing
            print("\n" + "-" * 40)

            # Small delay to prevent CPU overload
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nMonitor stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you're running with proper permissions (sudo)")
    finally:
        # Clean up GPIOs
        for gpio in gpios.values():
            try:
                gpio.close()
            except Exception:
                pass
        print("GPIOs cleaned up")


if __name__ == "__main__":
    monitor_gpio_status()

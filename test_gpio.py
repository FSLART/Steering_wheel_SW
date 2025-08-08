#!/usr/bin/env python3
"""
GPIO Test Script for Steering Wheel Dashboard
Tests GPIO buttons: Next, Back, OK, Cancel
Pin mapping: Next=14, Back=13, OK=11, Cancel=12
"""

import time
from periphery import GPIO


def test_gpio_buttons():
    """Test GPIO buttons with real-time feedback"""

    print("=" * 50)
    print("GPIO BUTTON TEST SCRIPT")
    print("=" * 50)
    print("Pin Mapping:")
    print("  - Next Button:   GPIO 14")
    print("  - Back Button:   GPIO 13")
    print("  - OK Button:     GPIO 11")
    print("  - Cancel Button: GPIO 12")
    print("=" * 50)
    print("Press CTRL+C to exit")
    print("=" * 50)

    # Initialize GPIOs
    try:
        gpio_next = GPIO(14, "in")
        gpio_back = GPIO(13, "in")
        gpio_ok = GPIO(11, "in")
        gpio_cancel = GPIO(12, "in")

        # Configure edge detection
        gpio_next.edge = "rising"
        gpio_back.edge = "rising"
        gpio_ok.edge = "rising"
        gpio_cancel.edge = "rising"

        print("✓ GPIOs initialized successfully")
        print("\nTesting buttons (press any button to see output):")
        print("Format: [TIMESTAMP] BUTTON_NAME: STATE")
        print("-" * 50)

        # Previous states for edge detection
        prev_next = 0
        prev_back = 0
        prev_ok = 0
        prev_cancel = 0

        button_press_count = {"next": 0, "back": 0, "ok": 0, "cancel": 0}

        while True:
            try:
                # Read current GPIO states
                next_state = gpio_next.read()
                back_state = gpio_back.read()
                ok_state = gpio_ok.read()
                cancel_state = gpio_cancel.read()

                current_time = time.strftime("%H:%M:%S")

                # Rising edge detection for Next button
                if next_state and not prev_next:
                    button_press_count["next"] += 1
                    print(
                        f"[{current_time}] NEXT BUTTON: PRESSED (Count: {button_press_count['next']})"
                    )
                elif not next_state and prev_next:
                    print(f"[{current_time}] NEXT BUTTON: RELEASED")
                prev_next = next_state

                # Rising edge detection for Back button
                if back_state and not prev_back:
                    button_press_count["back"] += 1
                    print(
                        f"[{current_time}] BACK BUTTON: PRESSED (Count: {button_press_count['back']})"
                    )
                elif not back_state and prev_back:
                    print(f"[{current_time}] BACK BUTTON: RELEASED")
                prev_back = back_state

                # Rising edge detection for OK button
                if ok_state and not prev_ok:
                    button_press_count["ok"] += 1
                    print(
                        f"[{current_time}] OK BUTTON: PRESSED (Count: {button_press_count['ok']})"
                    )
                elif not ok_state and prev_ok:
                    print(f"[{current_time}] OK BUTTON: RELEASED")
                prev_ok = ok_state

                # Rising edge detection for Cancel button
                if cancel_state and not prev_cancel:
                    button_press_count["cancel"] += 1
                    print(
                        f"[{current_time}] CANCEL BUTTON: PRESSED (Count: {button_press_count['cancel']})"
                    )
                elif not cancel_state and prev_cancel:
                    print(f"[{current_time}] CANCEL BUTTON: RELEASED")
                prev_cancel = cancel_state

                # Small delay to prevent overwhelming output
                time.sleep(0.05)  # 50ms polling

            except Exception as e:
                print(f"Error reading GPIOs: {e}")
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("TEST SUMMARY:")
        print(f"  Next Button Presses:   {button_press_count['next']}")
        print(f"  Back Button Presses:   {button_press_count['back']}")
        print(f"  OK Button Presses:     {button_press_count['ok']}")
        print(f"  Cancel Button Presses: {button_press_count['cancel']}")
        print("=" * 50)
        print("GPIO test stopped by user")

    except Exception as e:
        print(f"✗ GPIO initialization failed: {e}")
        print("\nPossible issues:")
        print("  - Check if running with proper permissions (sudo)")
        print("  - Verify GPIO pins are not in use by other processes")
        print("  - Check hardware connections")
        return False

    finally:
        try:
            # Clean up GPIOs
            gpio_next.close()
            gpio_back.close()
            gpio_ok.close()
            gpio_cancel.close()
            print("✓ GPIOs cleaned up successfully")
        except Exception:
            pass

    return True


def test_individual_gpio(pin_number):
    """Test a single GPIO pin"""
    print(f"Testing GPIO {pin_number} individually...")
    print("Press CTRL+C to stop")

    try:
        gpio = GPIO(pin_number, "in")
        gpio.edge = "both"  # Detect both rising and falling edges

        prev_state = gpio.read()
        print(f"Initial state: {prev_state}")

        while True:
            current_state = gpio.read()
            if current_state != prev_state:
                timestamp = time.strftime("%H:%M:%S")
                state_text = "HIGH" if current_state else "LOW"
                print(f"[{timestamp}] GPIO {pin_number}: {state_text}")
                prev_state = current_state
            time.sleep(0.01)

    except KeyboardInterrupt:
        print(f"\nStopped testing GPIO {pin_number}")
    except Exception as e:
        print(f"Error testing GPIO {pin_number}: {e}")
    finally:
        try:
            gpio.close()
        except Exception:
            pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Test individual GPIO
        try:
            pin = int(sys.argv[1])
            test_individual_gpio(pin)
        except ValueError:
            print("Usage: python test_gpio.py [pin_number]")
            print("Example: python test_gpio.py 14")
    else:
        # Test all GPIO buttons
        test_gpio_buttons()

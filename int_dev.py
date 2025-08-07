import customtkinter as ctk
import time
import threading
import random
import math
from windows import (
    create_debug_window,
    create_calibration_window,
    create_autonomous_window,
    create_main_dashboard,
)


# Mock classes for development
class MockGPIO:
    def __init__(self, pin, direction):
        self.pin = pin
        self.direction = direction
        self.edge = None
        self._state = 0

    def read(self):
        # Simulate random button presses for testing
        return random.choice([0, 0, 0, 0, 1]) if random.random() < 0.01 else 0


# Mock data structures
signal_values = {}
message_signals = {}
watched_ids = [0x20, 0x21, 0x22, 0x23, 0x24, 0x60, 0x69]
can_activity_state = {"active": True}
error_flags = {}
heartbeat_timestamps = {}
module_last_state = {}


# Mock CAN data generator
def generate_mock_can_data():
    """Generate realistic mock CAN data for testing"""
    while True:
        # Simulate voltage data (24V system: 20-28V range)
        voltage_base = 24.5
        voltage_variation = math.sin(time.time() * 0.1) * 2  # Slow oscillation
        signal_values["LV_Voltage"] = voltage_base + voltage_variation

        # Simulate RPM (0-6000 range with some variation)
        rpm_base = 2000 + math.sin(time.time() * 0.5) * 1500
        signal_values["RPM"] = max(0, rpm_base + random.randint(-200, 200))

        # Simulate temperatures
        signal_values["INV_Temperature"] = 450 + random.randint(-50, 100)  # 45°C base
        signal_values["Motor_Temperature"] = 600 + random.randint(
            -100, 200
        )  # 60°C base

        # Simulate other data
        signal_values["BPS"] = random.choice([0, 1])
        signal_values["SOC_HV"] = 75 + random.randint(-10, 15)  # 75% base
        signal_values["R2D"] = random.choice([0, 0, 0, 1])  # Mostly not ready
        signal_values["TRGT_Power"] = random.randint(0, 80)
        signal_values["LMT1"] = random.randint(0, 100)

        # Simulate autonomous mode data
        signal_values["Jerson_State"] = random.choice(
            [0, 1, 2]
        )  # 0=Error, 1=OK, 2=Warning
        signal_values["ACU_State"] = random.choice([0, 1, 2])
        signal_values["VCU_State"] = random.choice([0, 1, 2])
        signal_values["Maxon_State"] = random.choice(
            [0, 1, 2]
        )  # 0=Error, 1=OK, 2=Warning

        # Simulate pressure data (in bar, typical ranges for F1 systems)
        signal_values["Hydraulic_Front"] = 150 + random.randint(-20, 30)  # 130-180 bar
        signal_values["Hydraulic_Rear"] = 145 + random.randint(-15, 25)  # 130-170 bar
        signal_values["Pneumatic_Front"] = 8.5 + random.uniform(-1.0, 1.5)  # 7.5-10 bar
        signal_values["Pneumatic_Rear"] = 8.2 + random.uniform(-0.8, 1.3)  # 7.4-9.5 bar

        # Autonomous mode status
        signal_values["Autonomous_Mode"] = random.choice([0, 0, 0, 1])  # Mostly manual

        can_activity_state["active"] = True
        time.sleep(0.1)  # Update every 100ms


# Start mock data generator
threading.Thread(target=generate_mock_can_data, daemon=True).start()

# Set up CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create main dashboard
app = create_main_dashboard(signal_values, can_activity_state)

# Window management variables
debug_window = None
calibration_window = None
autonomous_window = None


# Mock GPIO monitoring (keyboard simulation)
def monitor_mock_buttons():
    """Simulate button presses for development"""
    window = 0

    def on_key_press(event):
        nonlocal window
        key = event.keysym.lower()

        if key == "right" or key == "n":  # Next
            window = (window + 1) % 4  # Changed to 4 windows
            update_window_state(window)
        elif key == "left" or key == "b":  # Back
            window = (window - 1) % 4  # Changed to 4 windows
            update_window_state(window)
        elif key == "escape":  # Close all windows
            window = 0
            update_window_state(window)

    def update_window_state(window):
        # Close all windows first with error handling
        try:
            app.after(0, close_calibration_window)
            app.after(0, close_debug_window)
            app.after(0, close_autonomous_window)
        except:
            pass

        # Then open the requested window with more delay
        if window == 0:
            # Main dashboard - all windows already closed
            app.after(0, app.focus_force)
            app.after(0, app.lift)
        elif window == 1:
            app.after(
                50, open_autonomous_window
            )  # Increased delay to ensure close completes first
        elif window == 2:
            app.after(50, open_calibration_window)
        elif window == 3:
            app.after(50, open_debug_window)

    # Bind keyboard events
    app.bind("<Key>", on_key_press)
    app.focus_set()


def open_debug_window():
    global debug_window
    try:
        if debug_window is None or not debug_window.winfo_exists():
            debug_window = create_debug_window(app, signal_values, watched_ids)
    except Exception as e:
        print(f"Error opening debug window: {e}")
        debug_window = None


def close_debug_window():
    global debug_window
    if debug_window is not None:
        try:
            if debug_window.winfo_exists():
                debug_window.destroy()
        except:
            pass
        debug_window = None


def open_calibration_window():
    global calibration_window
    try:
        if calibration_window is None or not calibration_window.winfo_exists():
            calibration_window = create_calibration_window(app)
    except Exception as e:
        print(f"Error opening calibration window: {e}")
        calibration_window = None


def close_calibration_window():
    global calibration_window
    if calibration_window is not None:
        try:
            if calibration_window.winfo_exists():
                calibration_window.destroy()
        except:
            pass
        calibration_window = None


def open_autonomous_window():
    global autonomous_window
    try:
        if autonomous_window is None or not autonomous_window.winfo_exists():
            autonomous_window = create_autonomous_window(app, signal_values)
    except Exception as e:
        print(f"Error opening autonomous window: {e}")
        autonomous_window = None


def close_autonomous_window():
    global autonomous_window
    if autonomous_window is not None:
        try:
            if autonomous_window.winfo_exists():
                autonomous_window.destroy()
        except:
            pass
        autonomous_window = None


# Start mock button monitoring
monitor_mock_buttons()

print("=" * 50)
print("DASHBOARD DEV MODE STARTED")
print("=" * 50)
print("Controls:")
print("  - Left/Right arrows (or B/N keys): Switch between windows")
print("    Window 0: Main Dashboard")
print("    Window 1: CAN Debug Monitor")
print("    Window 2: Calibration")
print("    Window 3: Autonomous Mode")
print("  - ESC: Close all windows and return to main")
print("  - Close window to exit")
print("=" * 50)

app.mainloop()

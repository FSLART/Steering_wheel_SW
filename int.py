import customtkinter as ctk
import time
import threading
from periphery import GPIO
from state_tracker import error_flags, heartbeat_timestamps, module_last_state
from can_receiver import (
    CANSignalReceiver,
    signal_values,
    message_signals,
    watched_ids,
    send_message,
    can_activity,
)
from rotary import RotarySwitch
from windows import (
    create_debug_window,
    create_calibration_window,
    create_autonomous_window,
    create_main_dashboard,
)

# rotary = RotarySwitch()
# rotary.start()

ctk.set_appearance_mode("dark")  # or "dark"
ctk.set_default_color_theme(
    "blue"
)  # Test different themes: "blue", "green", "dark-blue"

CANSignalReceiver()

# Start Main Window and Window Attributes
app = ctk.CTk()
app.geometry("800x480")
app.title("Dashboard")
app.attributes("-fullscreen", True)  # Set to fullscreen mode
app.configure(cursor="none")

# RPM Shift Lights - 12 circles
shift_lights = []
for i in range(12):
    x_pos = 100 + (i * 50)  # Space circles 50 pixels apart, starting at x=100
    circle = ctk.CTkLabel(
        app,
        text="●",
        font=("Noto Sans Bold", 40, "bold"),
        text_color="gray30",  # Default off color
    )
    circle.place(x=x_pos, y=15, anchor="center")
    shift_lights.append(circle)

# R2D WARNING - moved to bottom
R2D_label = ctk.CTkLabel(
    app,
    text="R2D STATE UNKNOWN",
    font=("Noto Sans Bold", 30, "bold"),
    text_color="purple",
)
R2D_label.place(relx=0.5, rely=0.96, anchor="center")


# Function to get color based on RPM value
can_indicator = ctk.CTkLabel(
    app,
    text="●",
    font=("Noto Sans Bold", 15, "bold"),
    text_color="red",
)
can_indicator.place(x=5, y=5)

# Main Frame
frame = ctk.CTkFrame(app, width=600, height=400)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Variables
rect_width = 160
rect_height = 80
speed = "ERR"  # Initial speed value for debugging

soc_lv_level = 0
soc_hv_level = 0

data_1 = "ERR"
data_2 = "ERR"
data_3 = "ERR"
data_4 = "ERR"
data_5 = "ERR"
data_6 = "ERR"
data_7 = 4

low_soc_lv_alert_shown = False
low_soc_hv_alert_shown = False
can_blink_state = False  # For blinking effect
last_can_activity = time.time()  # Initialize to current time to avoid immediate timeout

# Rectangle 1 - DATA XXXXXX
rect_1 = ctk.CTkFrame(
    frame, width=rect_width, height=rect_height, corner_radius=15
)  # Create a rectangle
rect_1.place(x=10, y=10)  # Position of the rectangle
title_1 = ctk.CTkLabel(
    rect_1, text="Temp INV ", font=("Noto Sans Bold ", 18)
)  # Create a Label
title_1.place(relx=0.5, rely=0.25, anchor="center")  # Position of the Label
data_label_1 = ctk.CTkLabel(rect_1, text=data_1, font=("Noto Sans Bold ", 40, "bold"))
data_label_1.place(relx=0.5, rely=0.65, anchor="center")

# Rectangle 2 - DATA XXXXX
rect_2 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_2.place(x=220, y=10)
title_2 = ctk.CTkLabel(
    rect_2, text="Temp Motor", font=("Noto Sans Bold ", 18)
)  # Create a Label
title_2.place(relx=0.5, rely=0.25, anchor="center")
data_label_2 = ctk.CTkLabel(rect_2, text=data_2, font=("Noto Sans Bold ", 40, "bold"))
data_label_2.place(relx=0.5, rely=0.65, anchor="center")

# Rectangle 3 - DATA XXXXXX
rect_3 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_3.place(x=430, y=10)
title_3 = ctk.CTkLabel(
    rect_3, text="BPS", font=("Noto Sans Bold ", 18)
)  # Create a Label
title_3.place(relx=0.5, rely=0.25, anchor="center")
data_label_3 = ctk.CTkLabel(rect_3, text=data_3, font=("Noto Sans Bold ", 40, "bold"))
data_label_3.place(relx=0.5, rely=0.65, anchor="center")

# Rectangle 4 - Kw Inst.
rect_4 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_4.place(x=10, rely=0.75)
title_4 = ctk.CTkLabel(rect_4, text="Kw Inst:", font=("Noto Sans Bold ", 24))
title_4.place(relx=0.3, rely=0.5, anchor="center")
data_label_4 = ctk.CTkLabel(rect_4, text=data_4, font=("Noto Sans Bold ", 50, "bold"))
data_label_4.place(relx=0.7, rely=0.5, anchor="center")

# Rectangle 5 - Kw Limit
rect_5 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_5.place(x=305, rely=0.75)
title_5 = ctk.CTkLabel(rect_5, text="Kw Limit:", font=("Noto Sans Bold ", 24))
title_5.place(relx=0.3, rely=0.5, anchor="center")
data_label_5 = ctk.CTkLabel(rect_5, text=data_5, font=("Noto Sans Bold ", 50, "bold"))
data_label_5.place(relx=0.7, rely=0.5, anchor="center")


##### SoC Bars #####

soc_LV_bar_label = ctk.CTkLabel(
    app, text="LV", font=("Noto Sans Bold ", 35, "bold")
)  # Create top label for the bar
soc_LV_bar_label.place(x=50, y=50, anchor="center")  # Center the label with the bar
soc_LV_bar = ctk.CTkProgressBar(
    app,
    orientation="vertical",
    width=60,
    height=320,
    corner_radius=4,
    progress_color="yellow",
)  # Create the bar
soc_LV_bar.place(x=20, y=80)  # Position the bar
soc_LV_bar.set(soc_lv_level / 100)  # Set the bar level based on SoC value (0-1 scale)
soc_LV_per = ctk.CTkLabel(
    app, text=str(int(soc_lv_level)) + "%", font=("Noto Sans Bold ", 28, "bold")
)  # Create Label inside the bar (smaller font for voltage + percentage)
soc_LV_per.place(x=50, y=430, anchor="center")  # Position the label inside the bar

soc_HV_bar_label = ctk.CTkLabel(app, text="HV", font=("Noto Sans Bold ", 35, "bold"))
soc_HV_bar_label.place(x=750, y=50, anchor="center")  # Center the label with the bar
soc_HV_bar = ctk.CTkProgressBar(
    app,
    orientation="vertical",
    width=60,
    height=320,
    corner_radius=4,
    progress_color="yellow",
)
soc_HV_bar.place(x=723, y=80)
soc_HV_bar.set(soc_hv_level / 100)  # Set the bar level based on SoC value (0-1 scale)
soc_HV_per = ctk.CTkLabel(
    app, text=str(int(soc_hv_level)) + "%", font=("Noto Sans Bold ", 37, "bold")
)
soc_HV_per.place(x=750, y=430, anchor="center")

# Speed and Units
speed_label = ctk.CTkLabel(
    frame, text=str(speed), font=("Noto Sans Bold ", 130, "bold")
)
speed_label.place(relx=0.5, rely=0.5, anchor="center")
speed_unit = ctk.CTkLabel(frame, text="Km/h", font=("Noto Sans Bold ", 30, "bold"))
speed_unit.place(relx=0.75, rely=0.60, anchor="center")

debug_window = None
calibration_window = None
autonomous_window = None


def monitor_gpio_buttons():
    # Open GPIOs once
    gpio_next = GPIO(14, "in")  # Adjust pin numbers if needed
    gpio_back = GPIO(13, "in")
    gpio_ok = GPIO(11, "in")
    gpio_cancel = GPIO(12, "in")
    gpio_next.edge = "rising"
    gpio_back.edge = "rising"
    gpio_ok.edge = "rising"
    gpio_cancel.edge = "rising"

    prev_next = 0
    prev_back = 0
    prev_ok = 0
    prev_cancel = 0
    window = 0

    while True:
        try:
            state_changed = False

            # Read current GPIO state
            next_state = gpio_next.read()
            back_state = gpio_back.read()

            # Rising edge detection for Next button
            if next_state and not prev_next:
                window = (window + 1) % 4  # Changed to 4 windows
                state_changed = True
            prev_next = next_state

            # Rising edge detection for Back button
            if back_state and not prev_back:
                window = (window - 1) % 4  # Changed to 4 windows
                state_changed = True
            prev_back = back_state

            if state_changed:
                # Close all windows first with error handling
                try:
                    app.after(0, close_calibration_window)
                    app.after(0, close_debug_window)
                    app.after(0, close_autonomous_window)
                except Exception:
                    pass

                # Then open the requested window
                if window == 0:
                    # Main dashboard - all windows already closed
                    app.after(0, app.focus_force)
                    app.after(0, app.lift)
                elif window == 1:
                    app.after(50, open_autonomous_window)
                elif window == 2:
                    app.after(50, open_calibration_window)
                elif window == 3:
                    app.after(50, open_debug_window)
        except Exception as e:
            print(f"GPIO monitor error: {e}")

        time.sleep(0.1)  # Polling interval


def check_speed():  # Update speed unit position for triple-digit speeds
    if speed != "ERR":
        if speed > 100:
            speed_unit.place(
                relx=0.77, rely=0.7, anchor="center"
            )  # Adjust position for larger speed values
        else:
            speed_unit.place(relx=0.7, rely=0.65, anchor="center")  # Default position
        frame.after(
            50, check_speed
        )  # Schedule the function to be called again after 50 ms


check_speed()

# def show_error_popup(msg_text):
#    popup = ctk.CTkToplevel(app)
#    popup.geometry("300x100")
#    popup.title("ERROR")
#    label = ctk.CTkLabel(popup, text=msg_text, font=("Noto Sans Bold", 18, "bold"))
#    label.pack(expand=True)
#    popup.lift()
#    popup.attributes("-topmost", True)
#    popup.focus()
#    popup.transient(app)
#    popup.grab_set()
#    popup.focus_force()
#
#    def close_after_10s():
#        popup.destroy()
#
#    popup.after(10000, close_after_10s)
rotory = 0


def update_data():
    global speed
    global data_1, data_2, data_3, data_4, data_5, data_6
    global soc_lv_level, soc_hv_level
    global low_soc_lv_alert_shown, low_soc_hv_alert_shown
    global rotory, can_activity, can_blink_state, last_can_activity

    current_time = time.time()

    # Enhanced CAN activity monitoring with timeout detection
    if can_activity:
        last_can_activity = current_time
        # Toggle between green and lime for blinking when active
        can_blink_state = not can_blink_state
        if can_blink_state:
            can_indicator.configure(text_color="lime")  # Bright green
        else:
            can_indicator.configure(text_color="green")  # Normal green
        can_activity = False  # Reset flag
    elif current_time - last_can_activity > 2.0:  # No activity for 2+ seconds
        # Orange for connection timeout
        can_indicator.configure(text_color="orange")
    else:
        # Red when no recent activity (but within timeout)
        can_indicator.configure(text_color="red")

    if "RPM" in signal_values:
        rpm_value = signal_values["RPM"]

        # Handle negative RPM values (overflow protection)
        if rpm_value != "ERR" and isinstance(rpm_value, (int, float)):
            # Check for overflow (negative values appearing as large positive numbers)
            if rpm_value > 32767:  # Likely a negative value wrapped around
                rpm_value = 0
            elif rpm_value < 0:  # Direct negative value
                rpm_value = 0

        speed = round(
            rpm_value * 0.02454, 1
        )  # Convert RPM to km/h (1000 RPM = 24.54 km/h)

        # Update RPM shift lights (max RPM is 6500, min is 0)
        if rpm_value != "ERR" and isinstance(rpm_value, (int, float)):
            # Calculate how many lights should be on (0-12)
            lights_on = int((rpm_value / 5000) * 12)
            lights_on = min(lights_on, 12)  # Cap at 12 lights

            # Update each shift light
            for i, light in enumerate(shift_lights):
                if i < lights_on:
                    # Determine color based on position (4 colors across 12 lights) - maximum saturation
                    if i < 3:  # First 3 lights - maximum saturated green
                        light.configure(text_color="#00FF00")  # Pure saturated green
                    elif i < 6:  # Next 3 lights - maximum saturated yellow
                        light.configure(text_color="#FFFF00")  # Pure saturated yellow
                    elif i < 9:  # Next 3 lights - maximum saturated red
                        light.configure(text_color="#FF0000")  # Pure saturated red
                    else:  # Last 3 lights - maximum saturated cyan (more vibrant than blue)
                        light.configure(text_color="#00FFFF")  # Pure saturated cyan
                else:
                    # Light is off
                    light.configure(text_color="gray30")
        else:
            # Turn off all lights when RPM is error
            for light in shift_lights:
                light.configure(text_color="gray30")
    # if "LV_SOC" in signal_values:
    #    soc_lv_level = signal_values["LV_SOC"]  # Update SoC LV level

    # Handle LV voltage for voltage-based percentage calculation
    if "LV_Voltage" in signal_values:
        lv_voltage_raw = signal_values["LV_Voltage"]

        if (
            lv_voltage_raw != "ERR"
            and isinstance(lv_voltage_raw, (int, float))
            and lv_voltage_raw > 0
        ):
            # Voltage is already scaled in can_receiver.py (divided by 1000)
            lv_voltage = lv_voltage_raw

            # Sanity check: voltage should be in reasonable range (15V-35V for 24V system)
            if 15.0 <= lv_voltage <= 35.0:
                # Calculate percentage based on voltage (24V system)
                min_voltage = 20.0  # Minimum voltage (0%) - adjusted for 24V system
                max_voltage = 28.8  # Maximum voltage (100%) - fully charged 24V

                # Calculate percentage based on voltage range
                voltage_percentage = (
                    (lv_voltage - min_voltage) / (max_voltage - min_voltage)
                ) * 100
                voltage_percentage = max(
                    0, min(100, voltage_percentage)
                )  # Clamp between 0-100%

                # Update the LV bar with voltage-based percentage
                soc_lv_level = voltage_percentage
            else:
                print(f"Warning: LV voltage out of range: {lv_voltage}V")
                lv_voltage = "ERR"
        else:
            lv_voltage = "ERR"
    if "SOC_HV" in signal_values:
        soc_hv_level = signal_values["SOC_HV"]  # Update SoC HV level

    # Check R2D state from both manual and auto signals (VCU_IGN_R2D message ID 1536)
    r2d_manual = signal_values.get("r2d_manual", 0)
    r2d_auto = signal_values.get("r2d_auto", 0)

    if "r2d_manual" in signal_values or "r2d_auto" in signal_values:
        # R2D is ready if either manual or auto R2D is active
        if r2d_manual == 1 or r2d_auto == 1:
            R2D_label.configure(
                text="READY", text_color="#00FF00"
            )  # Maximum saturated green
        else:
            R2D_label.configure(
                text="NOT READY", text_color="#FF0000"
            )  # Maximum saturated red
    elif "R2D" in signal_values:
        # Fallback to legacy R2D signal if available
        r2d_state = signal_values["R2D"]
        if r2d_state == 1:
            R2D_label.configure(
                text="READY", text_color="#00FF00"
            )  # Maximum saturated green
        else:
            R2D_label.configure(
                text="NOT READY", text_color="#FF0000"
            )  # Maximum saturated red
    else:
        # No R2D signal available
        R2D_label.configure(
            text="R2D STATE UNKNOWN", text_color="#FF00D9"
        )  # Maximum saturated magenta
    if "INV_Temperature" in signal_values:
        data_1 = signal_values["INV_Temperature"]  # Update Temp 1
    if "Motor_Temperature" in signal_values:
        data_2 = signal_values["Motor_Temperature"]  # Update Temp COLD
    if "BPS" in signal_values:
        data_3 = signal_values["BPS"]  # Update Temp 3
    if "TRGT_Power" in signal_values:
        data_4 = signal_values["TRGT_Power"]  # Update Kw Inst.
    if "LMT1" in signal_values:
        data_5 = signal_values["LMT1"]  # Update Kw Limzit

    # Process autonomous mode data if available
    # These signals should come from CAN when in autonomous mode
    if "Jerson_State" in signal_values:
        pass  # Autonomous window will handle display
    if "ACU_State" in signal_values:
        pass  # Autonomous window will handle display
    if "VCU_State" in signal_values:
        pass  # Autonomous window will handle display
    if "Maxon_State" in signal_values:
        pass  # Autonomous window will handle display
    if "Hydraulic_Front" in signal_values:
        pass  # Autonomous window will handle display
    if "Hydraulic_Rear" in signal_values:
        pass  # Autonomous window will handle display
    if "Pneumatic_Front" in signal_values:
        pass  # Autonomous window will handle display
    if "Pneumatic_Rear" in signal_values:
        pass  # Autonomous window will handle display

    speed_label.configure(text=str(speed))  # Update the speed display
    data_label_1.configure(text=str(data_1 / 10))  # Update Temp 1
    data_label_2.configure(text=str(data_2 / 10))  # Update Temp COLD
    data_label_3.configure(text=str(data_3))  # Update Temp 3
    data_label_4.configure(text=str(data_4))  # Update Kw Inst.
    data_label_5.configure(text=str(data_5))  # Update Kw Limit
    soc_HV_bar.set(soc_hv_level)  # Update SoC LV progress bar
    soc_LV_bar.set(soc_lv_level)  # Update SoC LV progress bar 

    if soc_hv_level != "ERR":
        soc_HV_per.configure(
            text=str(int(soc_hv_level)) + "%"
        )  # Update SoC HV percentage
        soc_HV_bar.set(soc_hv_level / 100)  # Update SoC HV progress bar (0-1 scale)

    if soc_lv_level != "ERR":
        # Check if we have voltage data to display
        if "LV_Voltage" in signal_values and signal_values["LV_Voltage"] != "ERR":
            lv_voltage = signal_values["LV_Voltage"]
            # Ensure voltage is valid before displaying
            if isinstance(lv_voltage, (int, float)) and 15.0 <= lv_voltage <= 35.0:
                # Display both voltage and percentage
                soc_LV_per.configure(
                    text=f"{lv_voltage:.1f}V\n{int(soc_lv_level)}%"
                )  # Show voltage and percentage
            else:
                # Invalid voltage, show error
                soc_LV_per.configure(text=f"ERR V\n{int(soc_lv_level)}%")
        else:
            # Fallback to just percentage if no voltage data
            soc_LV_per.configure(
                text=str(int(soc_lv_level)) + "%"
            )  # Update SoC LV percentage
        soc_LV_bar.set(soc_lv_level / 100)  # Update SoC LV progress bar (0-1 scale)
    else:
        # Both voltage and percentage are error
        soc_LV_per.configure(text="ERR")
        soc_LV_bar.set(0)  # Set bar to 0 when error
    # Check LV SoC
    if soc_lv_level < 0.2 and not low_soc_lv_alert_shown:
        # show_error_popup("SoC LV below 20%")
        low_soc_lv_alert_shown = True
    if soc_lv_level >= 0.2:
        low_soc_lv_alert_shown = False

    # Check HV SoC
    if soc_hv_level < 0.2 and not low_soc_hv_alert_shown:
        # show_error_popup("SoC HV below 20%")
        low_soc_hv_alert_shown = True
    if soc_hv_level >= 0.2:
        low_soc_hv_alert_shown = False

    # try:
    #   # index = rotary.get_index()
    #    if index is not None:
    #        if index == 0:
    #            rotory = 1
    #        elif index == 1:
    #            rotory = 0
    #        elif index == 2:
    #            rotory = 1
    #        elif index == 3:
    #            rotory = 0
    #        elif index == 4:
    #            rotory = 1
    #        elif index == 5:
    #            rotory = 0
    # except KeyboardInterrupt:
    #    print("Stopping...")
    #    #rotary.stop()

    # Send message VCU_2 with updated LMT1 value
    # send_message(
    #    "VCU_2",
    #    {
    #        "INV_Faults": 0,
    #        "LMT1": rotory,
    #        "LMT2": 0,
    #        "VCU_State": 1,
    #        "APPS_Error": 0,
    #        "Power_Plan": 2,
    #    },
    # )

    frame.after(50, update_data)  # Schedule the function to be called again after 5 ms


update_data()


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
    if debug_window is not None and debug_window.winfo_exists():
        debug_window.destroy()
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
    if calibration_window is not None and calibration_window.winfo_exists():
        calibration_window.destroy()
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
        except Exception:
            pass
        autonomous_window = None


def check_heartbeats():
    current_time = time.time()
    for module in [
        "MAP_DECODE_APPS_ERROR",
        "MAP_DECODE_VCU_ACU_STATE",
        "MAP_DECODE_INVERTER_ERROR",
        "MAP_DECODE_VCU_STATE",
        "MAP_DECODE_Ready2Drive_STATE",
    ]:
        if current_time - heartbeat_timestamps.get(module, current_time) > 30:
            if not error_flags.get(module, False):
                # show_error_popup(f"{module} heartbeat lost!")
                error_flags[module] = True
    app.after(1000, check_heartbeats)


check_heartbeats()

gpio_thread = threading.Thread(target=monitor_gpio_buttons, daemon=True)
gpio_thread.start()
app.mainloop()

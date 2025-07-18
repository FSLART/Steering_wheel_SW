import customtkinter as ctk
import time
import can
import threading
from cxxheaderparser.simple import parse_file  # Import cxxheaderparser
import os
import re
import random
import glob  # Import glob to handle multiple files
from can_parser import parse_can_header, decode_data, macros_by_id, decode_macros
from state_tracker import error_flags, heartbeat_timestamps, module_last_state

ctk.set_appearance_mode("dark")  # or "dark"
ctk.set_default_color_theme("blue")  # Test different themes: "blue", "green", "dark-blue"

# Start Main Window and Window Attributes
app = ctk.CTk()
app.geometry("800x480")
app.title("Dashboard")
app.config(cursor="none")  # Hide the mouse cursor
app.attributes("-fullscreen", True)  # Set to fullscreen mode
# R2D WARNING
R2D_label = ctk.CTkLabel(app, text="R2D STATE UNKNOWN", font=("Noto Sans Bold", 30, "bold"), text_color="purple")
R2D_label.place(relx=0.5, rely=0.04, anchor="center")

# Main Frame
frame = ctk.CTkFrame(app, width=600, height=400)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Variables
rect_width = 160
rect_height = 80
speed = 36  # Initial speed value for debugging

soc_lv_level = 0.6
soc_hv_level = 0.78

data_1 = "ERR"
data_2 = "ERR"
data_3 = "ERR"
data_4 = "ERR"
data_5 = "ERR"
data_6 = "ERR"

low_soc_lv_alert_shown = False
low_soc_hv_alert_shown = False



# Rectangle 1 - DATA XXXXXX
rect_1 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)  # Create a rectangle
rect_1.place(x=10, y=10)  # Position of the rectangle
title_1 = ctk.CTkLabel(rect_1, text="Temp 1 ", font=("Noto Sans Bold ", 18))  # Create a Label
title_1.place(relx=0.5, rely=0.25, anchor='center')  # Position of the Label
data_label_1 = ctk.CTkLabel(rect_1, text=data_1, font=("Noto Sans Bold ", 40, "bold"))
data_label_1.place(relx=0.5, rely=0.65, anchor='center')

# Rectangle 2 - DATA XXXXX
rect_2 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_2.place(x=220, y=10)
title_2 = ctk.CTkLabel(rect_2, text="Temp COLD", font=("Noto Sans Bold ", 18))  # Create a Label
title_2.place(relx=0.5, rely=0.25, anchor='center')
data_label_2 = ctk.CTkLabel(rect_2, text=data_2, font=('Noto Sans Bold ', 40, 'bold'))
data_label_2.place(relx=0.5, rely=0.65, anchor='center')

# Rectangle 3 - DATA XXXXXX
rect_3 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_3.place(x=430, y=10)
title_3 = ctk.CTkLabel(rect_3, text="Temp 3", font=("Noto Sans Bold ", 18))  # Create a Label
title_3.place(relx=0.5, rely=0.25, anchor='center')
data_label_3 = ctk.CTkLabel(rect_3, text=data_3, font=("Noto Sans Bold ", 40, "bold"))
data_label_3.place(relx=0.5, rely=0.65, anchor='center')

# Rectangle 4 - Kw Inst.
rect_4 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_4.place(x=10, rely=0.75)
title_4 = ctk.CTkLabel(rect_4, text="Kw Inst:", font=("Noto Sans Bold ", 24))
title_4.place(relx=0.3, rely=0.5, anchor='center')
data_label_4 = ctk.CTkLabel(rect_4, text=data_4, font=("Noto Sans Bold ", 50, "bold"))
data_label_4.place(relx=0.7, rely=0.5, anchor='center')

# Rectangle 5 - Kw Limit
rect_5 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_5.place(x=305, rely=0.75)
title_5 = ctk.CTkLabel(rect_5, text="Kw Limit:", font=("Noto Sans Bold ", 24))
title_5.place(relx=0.3, rely=0.5, anchor='center')
data_label_5 = ctk.CTkLabel(rect_5, text=data_5, font=("Noto Sans Bold ", 50, "bold"))
data_label_5.place(relx=0.7, rely=0.5, anchor='center')

##### SoC Bars #####

soc_LV_bar_label = ctk.CTkLabel(app, text="LV", font=("Noto Sans Bold ", 35, "bold"))  # Create top label for the bar
soc_LV_bar_label.place(x=50, y=50, anchor='center')  # Center the label with the bar
soc_LV_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4)  # Create the bar
soc_LV_bar.place(x=20, y=80)  # Position the bar
soc_LV_bar.set(soc_lv_level)  # Set the bar level based on SoC value
soc_LV_per = ctk.CTkLabel(app, text=str(int(soc_lv_level * 100)) + '%', font=("Noto Sans Bold ", 37, "bold"))  # Create Label inside the bar
soc_LV_per.place(x=50, y=430, anchor='center')  # Position the label inside the bar

soc_HV_bar_label = ctk.CTkLabel(app, text="HV", font=("Noto Sans Bold ", 35, "bold"))
soc_HV_bar_label.place(x=750, y=50, anchor='center')  # Center the label with the bar
soc_HV_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4)
soc_HV_bar.place(x=723, y=80)
soc_HV_bar.set(soc_hv_level)
soc_HV_per = ctk.CTkLabel(app, text=str(int(soc_hv_level * 100)) + '%', font=("Noto Sans Bold ", 37, "bold"))
soc_HV_per.place(x=750, y=430, anchor='center')

# Speed and Units
speed_label = ctk.CTkLabel(frame, text=str(speed), font=("Noto Sans Bold ", 130, "bold"))
speed_label.place(relx=0.5, rely=0.5, anchor='center')
speed_unit = ctk.CTkLabel(frame, text="Km/h", font=("Noto Sans Bold ", 30, "bold"))
speed_unit.place(relx=0.75, rely=0.60, anchor='center')

def check_speed():  # Update speed unit position for triple-digit speeds
    if speed > 100:
        speed_unit.place(relx=0.77, rely=0.7, anchor='center')  # Adjust position for larger speed values
    else:
        speed_unit.place(relx=0.7, rely=0.65, anchor='center')  # Default position
    frame.after(50, check_speed)  # Schedule the function to be called again after 50 ms

check_speed()

def show_error_popup(msg_text):
    popup = ctk.CTkToplevel(app)
    popup.geometry("300x100")
    popup.title("ERROR")
    label = ctk.CTkLabel(popup, text=msg_text, font=("Noto Sans Bold", 18, "bold"))
    label.pack(expand=True)
    popup.lift()
    popup.attributes("-topmost", True)
    popup.focus()
    popup.transient(app)
    popup.grab_set()
    popup.focus_force()

    def close_after_10s():
        popup.destroy()

    popup.after(10000, close_after_10s)


def update_data():
    global speed
    global data_1, data_2, data_3, data_4, data_5, data_6
    global soc_lv_level, soc_hv_level
    global low_soc_lv_alert_shown, low_soc_hv_alert_shown

    speed_label.configure(text=str(speed))  # Update the speed display
    data_label_1.configure(text=str(data_1))  # Update Temp 1
    data_label_2.configure(text=str(data_2))  # Update Temp COLD
    data_label_3.configure(text=str(data_3))  # Update Temp 3
    data_label_4.configure(text=str(data_4))  # Update Kw Inst.
    data_label_5.configure(text=str(data_5))  # Update Kw Limit
    soc_HV_bar.set(soc_lv_level)  # Update SoC LV progress bar
    soc_HV_per.configure(text=str(int(soc_lv_level * 100)) + '%')  # Update SoC LV percentage
    soc_LV_bar.set(soc_hv_level)  # Update SoC HV progress bar
    soc_LV_per.configure(text=str(int(soc_hv_level * 100)) + '%')  # Update SoC HV percentage

    # Check LV SoC
    if soc_lv_level < 0.2 and not low_soc_lv_alert_shown:
        show_error_popup("SoC LV below 20%")
        low_soc_lv_alert_shown = True
    if soc_lv_level >= 0.2:
        low_soc_lv_alert_shown = False

    # Check HV SoC
    if soc_hv_level < 0.2 and not low_soc_hv_alert_shown:
        show_error_popup("SoC HV below 20%")
        low_soc_hv_alert_shown = True
    if soc_hv_level >= 0.2:
        low_soc_hv_alert_shown = False

    frame.after(5, update_data)  # Schedule the function to be called again after 5 ms
#update_data()

######################################################################################################## Debug Window
def open_debug_window():
    debug_window = ctk.CTkToplevel(app)
    debug_window.geometry("800x480")
    debug_window.title("DEBUG")
    close_button = ctk.CTkButton(debug_window, text="Close", command=debug_window.destroy)  # Close Button
    close_button.place(y=450)

    # Create the header
    line = ctk.CTkFrame(debug_window, width=850, height=7, fg_color="black")
    line.place(x=-5, y=50)
    # Create the title label
    title_label = ctk.CTkLabel(debug_window, text="DEBUG", font=("Noto Sans Bold", 32, "bold"), bg_color="transparent")
    title_label.place(relx=0.5, y=23, anchor='center')

    # Display the current time on the far left of the header
    def update_time():
        current_time = time.strftime("%H:%M")
        time_label.configure(text=current_time)
        debug_window.after(1000, update_time)  # Update the time every second

    time_label = ctk.CTkLabel(debug_window, text="", font=("Noto Sans Bold", 27, "bold"))
    time_label.place(x=20, y=8)
    update_time()
    # Placeholder data for debugging
    categories = {
        "Cells": ["Cell Voltage", "Cell Temperature", "Cell Resistance"],
        "Drivetrain": ["Motor RPM", "Motor Temperature", "Torque"],
        "Test": ["Test Voltage", "Test Current", "Test Power"]
    }

    y_position = 80  # Initial y position for the first category

    for category, items in categories.items():
        # Create a frame for the category
        category_frame = ctk.CTkFrame(debug_window, width=350, height=len(items) * 30 + 50, corner_radius=10)
        category_frame.place(x=20 if category != "Test" else 420, y=y_position)

        # Create a label for the category
        category_label = ctk.CTkLabel(category_frame, text=category, font=("Noto Sans Bold", 20))
        category_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create labels for each item in the category
        for i, item in enumerate(items):
            item_label = ctk.CTkLabel(category_frame, text=item, font=("Noto Sans", 16))
            item_label.place(x=10, y=40 + i * 30)

        y_position += len(items) * 30 + 70  # Update y position for the next category

def open_calibration_window():
    calibration_window = ctk.CTkToplevel(app)
    calibration_window.geometry("800x480")
    calibration_window.title("CALIBRATION")
    # Removed the line setting the entire window background to black

    # Create the header frame
    header_frame = ctk.CTkFrame(calibration_window, width=800, height=60, fg_color="black")
    header_frame.place(x=0, y=0)

    # Create the title label
    title_label = ctk.CTkLabel(calibration_window, text="CALIBRATION", font=("Noto Sans Bold", 32, "bold"), bg_color="black")
    title_label.place(relx=0.5, y=23, anchor='center')

    # Function to flash the title label
    def flash_title():
        current_color = title_label.cget("text_color")
        new_color = "yellow" if current_color == "red" else "red"
        title_label.configure(text_color=new_color)
        calibration_window.after(300, flash_title)  # Flash every 300 ms

    flash_title()

    # Display the current time on the far left of the header
    def update_time():
        current_time = time.strftime("%H:%M")
        time_label.configure(text=current_time)
        calibration_window.after(1000, update_time)  # Update the time every second

    time_label = ctk.CTkLabel(calibration_window, text="", font=("Noto Sans Bold", 27, "bold"), text_color="white", bg_color="black")
    time_label.place(x=20, y=8)
    update_time()

    # Placeholder data for calibration
    categories = {
        "Cells": ["Cell Voltage", "Cell Temperature", "Cell Resistance"],
        "Drivetrain": ["Motor RPM", "Motor Temperature", "Torque"],
        "Test": ["Test Voltage", "Test Current", "Test Power"]
    }

    y_position = 80  # Initial y position for the first category

    for category, items in categories.items():
        # Create a frame for the category
        category_frame = ctk.CTkFrame(calibration_window, width=350, height=len(items) * 30 + 50, corner_radius=10)
        category_frame.place(x=20 if category != "Test" else 420, y=y_position)

        # Create a label for the category
        category_label = ctk.CTkLabel(category_frame, text=category, font=("Noto Sans Bold", 20))
        category_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create labels for each item in the category
        for i, item in enumerate(items):
            item_label = ctk.CTkLabel(category_frame, text=item, font=("Noto Sans", 16))
            item_label.place(x=10, y=40 + i * 30)

        y_position += len(items) * 30 + 70  # Update y position for the next category

##### PLACEHOLDER BUTTON TO OPEN DEBUG WINDOW #####
# Buttons to open the new windows
open_window_button = ctk.CTkButton(app, text="DEBUG", command=open_debug_window)
open_window_button.place(relx=0.4, rely=0.95, anchor='center')
open_calibration_button = ctk.CTkButton(app, text="CALIBRATION", command=open_calibration_window)
open_calibration_button.place(relx=0.7, rely=0.95, anchor='center')
###################################################

HEADER_FOLDER = "Can-Header-Map"  # Change from single file to folder
macros_by_id, decode_macros = parse_can_header(HEADER_FOLDER)

bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)

def check_heartbeats():
    current_time = time.time()
    for module in ["MAP_DECODE_APPS_ERROR", "MAP_DECODE_VCU_ACU_STATE", 
                   "MAP_DECODE_INVERTER_ERROR", "MAP_DECODE_VCU_STATE", "MAP_DECODE_Ready2Drive_STATE"]:
        if current_time - heartbeat_timestamps.get(module, current_time) > 30:
            if not error_flags.get(module, False):
                show_error_popup(f"{module} heartbeat lost!")
                error_flags[module] = True
    app.after(1000, check_heartbeats)
    
check_heartbeats()

def poll_can():
    msg = bus.recv(timeout=0.0)
    # Flush stale messages
    while True:
        new_msg = bus.recv(timeout=0.0)
        if not new_msg:
            break
        msg = new_msg
    if msg:
        update_gui(msg)
    app.after(50, poll_can)

last_r2d_state = None

def update_gui(msg):
    global data_1, data_2, data_3, data_4, data_5, data_6, last_r2d_state
    if msg.arbitration_id in macros_by_id:
        print(f"[DEBUG] Recognized ID={hex(msg.arbitration_id)}; Macros={macros_by_id[msg.arbitration_id]}")
        for macro_name in macros_by_id[msg.arbitration_id]:
            if macro_name not in decode_macros:
                continue  # Skip macros that don't have decode expressions
            expr = decode_macros[macro_name]
            result = decode_data(msg.data, expr)
            print(f"[DEBUG] Macro='{macro_name}' DecodedValue={result}")
            match macro_name:
                case "MAP_DECODE_MOTOR_TEMPERATURE":
                    data_1 = result
                    data_label_1.configure(text=str(result))  # Update Motor Temperature display
                case "MAP_DECODE_INVERTER_TEMPERATURE":
                    data_2 = result
                    data_label_2.configure(text=str(result))  # Update Inverter Temperature display
                case "MAP_DECODE_CONSUMED_POWER":
                    data_3 = result
                    data_label_3.configure(text=str(result))  # Update Consumed Power display
                    print(f"DecodedValue={result}")
                case "MAP_DECODE_TARGET_POWER":
                    data_4 = result
                    data_label_4.configure(text=str(result))  # Update Target Power display
                case "MAP_DECODE_DATA_LOGGER_STATE":
                    if result == 1:
                        data_logger_dot = ctk.CTkLabel(app, text="●", font=("Noto Sans Bold", 25), text_color="yellow")
                        data_logger_dot.place(x=10, y=10)
                    else:
                        if 'data_logger_dot' in globals():
                            data_logger_dot.place_forget()
                case "MAP_DECODE_Ready2Drive_STATE":
                    # Update heartbeat for R2D state
                    heartbeat_timestamps["MAP_DECODE_Ready2Drive_STATE"] = time.time()
                    # Existing logic remains intact:
                    if result != last_r2d_state:
                        global blink_id
                        if 'blink_id' in globals() and blink_id is not None:
                            R2D_label.after_cancel(blink_id)
                            blink_id = None

                        if result == 1:
                            R2D_label.configure(text="R2D", text_color="green")
                            R2D_label.place(relx=0.5, rely=0.04, anchor="center")
                        else:
                            global funny_message
                            funny_messages = [
                                "Out of Order (Try Again Later)",
                                "!READY2DRIVE",
                                "Nah, Lets Walk Instead",
                                "VCU is on Strike / VCU está em greve",
                                "ALERT: Car Identifies as a Park Bench"
                            ]
                            funny_message = random.choice(funny_messages)
                            R2D_label.configure(text=funny_message, text_color="red")
                            R2D_label.place(relx=0.5, rely=0.04, anchor="center")
                            
                            def blink_red():
                                global blink_id
                                if R2D_label.winfo_ismapped():
                                    R2D_label.place_forget()
                                else:
                                    R2D_label.configure(text=funny_message)
                                    R2D_label.place(relx=0.5, rely=0.04, anchor="center")
                                blink_id = R2D_label.after(1000, blink_red)
                                
                            blink_red()
                        last_r2d_state = result
                        
                case "MAP_DECODE_APPS_ERROR":
                    heartbeat_timestamps["MAP_DECODE_APPS_ERROR"] = time.time()
                    if result != module_last_state["MAP_DECODE_APPS_ERROR"]:
                        if result == 0:
                            show_error_popup("APPS module is dead!")
                        module_last_state["MAP_DECODE_APPS_ERROR"] = result

                case "MAP_DECODE_VCU_ACU_STATE":
                    heartbeat_timestamps["MAP_DECODE_VCU_ACU_STATE"] = time.time()
                    if result != module_last_state["MAP_DECODE_VCU_ACU_STATE"]:
                        if result == 0:
                            show_error_popup("VCU ACU module is dead!")
                        module_last_state["MAP_DECODE_VCU_ACU_STATE"] = result

                case "MAP_DECODE_INVERTER_ERROR":
                    heartbeat_timestamps["MAP_DECODE_INVERTER_ERROR"] = time.time()
                    if result != module_last_state["MAP_DECODE_INVERTER_ERROR"]:
                        if result == 0:
                            show_error_popup("Inverter module is dead!")
                        module_last_state["MAP_DECODE_INVERTER_ERROR"] = result

                case "MAP_DECODE_VCU_STATE":
                    heartbeat_timestamps["MAP_DECODE_VCU_STATE"] = time.time()
                    if result != module_last_state["MAP_DECODE_VCU_STATE"]:
                        if result == 0:
                            show_error_popup("VCU module is dead!")
                        module_last_state["MAP_DECODE_VCU_STATE"] = result

                case _:
                    pass # Ignore other macros

poll_can()
app.mainloop()

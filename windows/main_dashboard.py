import customtkinter as ctk
import time


def create_main_dashboard(signal_values, can_activity_state):
    """Create and return the main dashboard window"""
    app = ctk.CTk()
    app.geometry("800x480")
    app.title("Dashboard - DEV MODE")
    # Remove fullscreen for development
    # app.attributes("-fullscreen", True)
    app.configure(cursor="arrow")  # Show cursor for development

    # Variables
    rect_width = 160
    rect_height = 80
    speed = "ERR"

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
    can_blink_state = False
    last_can_activity = time.time()

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
        text_color="#FF00FF",  # Bright magenta
    )
    R2D_label.place(relx=0.5, rely=0.96, anchor="center")

    # CAN indicator
    can_indicator = ctk.CTkLabel(
        app,
        text="●",
        font=("Noto Sans Bold", 15, "bold"),
        text_color="#FF0000",  # Bright red
    )
    can_indicator.place(x=5, y=5)

    # DEV MODE indicator
    dev_label = ctk.CTkLabel(
        app,
        text="DEV MODE",
        font=("Noto Sans Bold", 12, "bold"),
        text_color="#FF4500",  # Bright orange
    )
    dev_label.place(x=5, y=25)

    # Main Frame
    frame = ctk.CTkFrame(app, width=600, height=400)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Rectangle 1 - DATA XXXXXX
    rect_1 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
    rect_1.place(x=10, y=10)
    title_1 = ctk.CTkLabel(rect_1, text="Temp INV ", font=("Noto Sans Bold ", 18))
    title_1.place(relx=0.5, rely=0.25, anchor="center")
    data_label_1 = ctk.CTkLabel(
        rect_1, text=data_1, font=("Noto Sans Bold ", 40, "bold")
    )
    data_label_1.place(relx=0.5, rely=0.65, anchor="center")

    # Rectangle 2 - DATA XXXXX
    rect_2 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
    rect_2.place(x=220, y=10)
    title_2 = ctk.CTkLabel(rect_2, text="Temp Motor", font=("Noto Sans Bold ", 18))
    title_2.place(relx=0.5, rely=0.25, anchor="center")
    data_label_2 = ctk.CTkLabel(
        rect_2, text=data_2, font=("Noto Sans Bold ", 40, "bold")
    )
    data_label_2.place(relx=0.5, rely=0.65, anchor="center")

    # Rectangle 3 - DATA XXXXXX
    rect_3 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
    rect_3.place(x=430, y=10)
    title_3 = ctk.CTkLabel(rect_3, text="BPS", font=("Noto Sans Bold ", 18))
    title_3.place(relx=0.5, rely=0.25, anchor="center")
    data_label_3 = ctk.CTkLabel(
        rect_3, text=data_3, font=("Noto Sans Bold ", 40, "bold")
    )
    data_label_3.place(relx=0.5, rely=0.65, anchor="center")

    # Rectangle 4 - Kw Inst.
    rect_4 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
    rect_4.place(x=10, rely=0.75)
    title_4 = ctk.CTkLabel(rect_4, text="Kw Inst:", font=("Noto Sans Bold ", 24))
    title_4.place(relx=0.3, rely=0.5, anchor="center")
    data_label_4 = ctk.CTkLabel(
        rect_4, text=data_4, font=("Noto Sans Bold ", 50, "bold")
    )
    data_label_4.place(relx=0.7, rely=0.5, anchor="center")

    # Rectangle 5 - Kw Limit
    rect_5 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
    rect_5.place(x=305, rely=0.75)
    title_5 = ctk.CTkLabel(rect_5, text="Kw Limit:", font=("Noto Sans Bold ", 24))
    title_5.place(relx=0.3, rely=0.5, anchor="center")
    data_label_5 = ctk.CTkLabel(
        rect_5, text=data_5, font=("Noto Sans Bold ", 50, "bold")
    )
    data_label_5.place(relx=0.7, rely=0.5, anchor="center")

    ##### SoC Bars #####

    soc_LV_bar_label = ctk.CTkLabel(
        app, text="LV", font=("Noto Sans Bold ", 35, "bold")
    )
    soc_LV_bar_label.place(x=50, y=50, anchor="center")
    soc_LV_bar = ctk.CTkProgressBar(
        app,
        orientation="vertical",
        width=60,
        height=320,
        corner_radius=4,
        progress_color="#FFFF00",  # Bright yellow
    )
    soc_LV_bar.place(x=20, y=80)
    soc_LV_bar.set(soc_lv_level / 100)
    soc_LV_per = ctk.CTkLabel(
        app, text=str(int(soc_lv_level)) + "%", font=("Noto Sans Bold ", 28, "bold")
    )
    soc_LV_per.place(x=50, y=430, anchor="center")

    soc_HV_bar_label = ctk.CTkLabel(
        app, text="HV", font=("Noto Sans Bold ", 35, "bold")
    )
    soc_HV_bar_label.place(x=750, y=50, anchor="center")
    soc_HV_bar = ctk.CTkProgressBar(
        app,
        orientation="vertical",
        width=60,
        height=320,
        corner_radius=4,
        progress_color="#FFFF00",  # Bright yellow
    )
    soc_HV_bar.place(x=723, y=80)
    soc_HV_bar.set(soc_hv_level / 100)
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

    # Add instructions label
    instructions = ctk.CTkLabel(
        app,
        text="DEV CONTROLS: ← → (or N/B) to switch windows (Main/Debug/Calibration/Autonomous), ESC to close all",
        font=("Noto Sans Bold", 9),
        text_color="#808080",  # Bright gray
    )
    instructions.place(x=10, y=460)

    def check_speed():
        nonlocal speed
        if speed != "ERR":
            if speed > 100:
                speed_unit.place(relx=0.77, rely=0.7, anchor="center")
            else:
                speed_unit.place(relx=0.7, rely=0.65, anchor="center")
            frame.after(50, check_speed)

    def update_data():
        nonlocal speed, data_1, data_2, data_3, data_4, data_5, data_6
        nonlocal \
            soc_lv_level, \
            soc_hv_level, \
            low_soc_lv_alert_shown, \
            low_soc_hv_alert_shown
        nonlocal can_blink_state, last_can_activity

        current_time = time.time()

        # Enhanced CAN activity monitoring with timeout detection
        if can_activity_state["active"]:
            last_can_activity = current_time
            can_blink_state = not can_blink_state
            if can_blink_state:
                can_indicator.configure(text_color="#00FF00")  # Bright lime
            else:
                can_indicator.configure(text_color="#32CD32")  # Lime green
            can_activity_state["active"] = False
        elif current_time - last_can_activity > 2.0:
            can_indicator.configure(text_color="#FF4500")  # Bright orange
        else:
            can_indicator.configure(text_color="#FF0000")  # Bright red

        if "RPM" in signal_values:
            rpm_value = signal_values["RPM"]

            if rpm_value != "ERR" and isinstance(rpm_value, (int, float)):
                if rpm_value > 32767:
                    rpm_value = 0
                elif rpm_value < 0:
                    rpm_value = 0

            speed = round(rpm_value * 0.02454, 1)

            if rpm_value != "ERR" and isinstance(rpm_value, (int, float)):
                lights_on = int((rpm_value / 5000) * 12)
                lights_on = min(lights_on, 12)

                for i, light in enumerate(shift_lights):
                    if i < lights_on:
                        if i < 3:
                            light.configure(text_color="#00FF00")
                        elif i < 6:
                            light.configure(text_color="#FFFF00")
                        elif i < 9:
                            light.configure(text_color="#FF0000")
                        else:
                            light.configure(text_color="#0000FF")
                    else:
                        light.configure(text_color="gray30")
            else:
                for light in shift_lights:
                    light.configure(text_color="gray30")

        # Handle LV voltage for voltage-based percentage calculation
        if "LV_Voltage" in signal_values:
            lv_voltage_raw = signal_values["LV_Voltage"]

            if (
                lv_voltage_raw != "ERR"
                and isinstance(lv_voltage_raw, (int, float))
                and lv_voltage_raw > 0
            ):
                lv_voltage = lv_voltage_raw

                if 15.0 <= lv_voltage <= 35.0:
                    min_voltage = 20.0
                    max_voltage = 28.8

                    voltage_percentage = (
                        (lv_voltage - min_voltage) / (max_voltage - min_voltage)
                    ) * 100
                    voltage_percentage = max(0, min(100, voltage_percentage))

                    soc_lv_level = voltage_percentage
                else:
                    print(f"Warning: LV voltage out of range: {lv_voltage}V")
                    lv_voltage = "ERR"
            else:
                lv_voltage = "ERR"

        if "SOC_HV" in signal_values:
            soc_hv_level = signal_values["SOC_HV"]

        if "R2D" in signal_values:
            r2d_state = signal_values["R2D"]
            if r2d_state == 1:
                R2D_label.configure(
                    text="READY TO DRIVE", text_color="#00FF00"
                )  # Bright green
            else:
                R2D_label.configure(
                    text="NOT READY", text_color="#FF0000"
                )  # Bright red
        else:
            R2D_label.configure(
                text="R2D STATE UNKNOWN", text_color="#FF00FF"
            )  # Bright magenta

        if "INV_Temperature" in signal_values:
            data_1 = signal_values["INV_Temperature"]
        if "Motor_Temperature" in signal_values:
            data_2 = signal_values["Motor_Temperature"]
        if "BPS" in signal_values:
            data_3 = signal_values["BPS"]
        if "TRGT_Power" in signal_values:
            data_4 = signal_values["TRGT_Power"]
        if "LMT1" in signal_values:
            data_5 = signal_values["LMT1"]

        speed_label.configure(text=str(speed))
        data_label_1.configure(text=str(data_1 / 10) if data_1 != "ERR" else "ERR")
        data_label_2.configure(text=str(data_2 / 10) if data_2 != "ERR" else "ERR")
        data_label_3.configure(text=str(data_3))
        data_label_4.configure(text=str(data_4))
        data_label_5.configure(text=str(data_5))

        if soc_hv_level != "ERR":
            soc_HV_per.configure(text=str(int(soc_hv_level)) + "%")
            soc_HV_bar.set(soc_hv_level / 100)

        if soc_lv_level != "ERR":
            if "LV_Voltage" in signal_values and signal_values["LV_Voltage"] != "ERR":
                lv_voltage = signal_values["LV_Voltage"]
                if isinstance(lv_voltage, (int, float)) and 15.0 <= lv_voltage <= 35.0:
                    soc_LV_per.configure(
                        text=f"{lv_voltage:.1f}V\n{int(soc_lv_level)}%"
                    )
                else:
                    soc_LV_per.configure(text=f"ERR V\n{int(soc_lv_level)}%")
            else:
                soc_LV_per.configure(text=str(int(soc_lv_level)) + "%")
            soc_LV_bar.set(soc_lv_level / 100)
        else:
            soc_LV_per.configure(text="ERR")
            soc_LV_bar.set(0)

        frame.after(50, update_data)

    # Start the update functions
    check_speed()
    update_data()

    return app

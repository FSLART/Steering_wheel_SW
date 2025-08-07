import customtkinter as ctk
import time


def create_calibration_window(parent_app):
    """Create and return the calibration window"""
    calibration_window = ctk.CTkToplevel(parent_app)
    calibration_window.geometry("800x480")
    calibration_window.title("CALIBRATION - DEV")
    calibration_window.configure(cursor="arrow")

    header_frame = ctk.CTkFrame(
        calibration_window,
        width=800,
        height=60,
        fg_color="#000000",  # Pure black
    )
    header_frame.place(x=0, y=0)

    title_label = ctk.CTkLabel(
        calibration_window,
        text="CALIBRATION (DEV)",
        font=("Noto Sans Bold", 32, "bold"),
        bg_color="#000000",  # Pure black
        text_color="#FF0000",  # Start with bright red
    )
    title_label.place(relx=0.5, y=23, anchor="center")

    def flash_title():
        current_color = title_label.cget("text_color")
        new_color = (
            "#FFFF00" if current_color == "#FF0000" else "#FF0000"
        )  # Bright yellow/red
        title_label.configure(text_color=new_color)
        calibration_window.after(300, flash_title)

    flash_title()

    def update_time():
        current_time = time.strftime("%H:%M")
        time_label.configure(text=current_time)
        calibration_window.after(1000, update_time)

    time_label = ctk.CTkLabel(
        calibration_window,
        text="",
        font=("Noto Sans Bold", 27, "bold"),
        text_color="#00FFFF",  # Bright cyan
        bg_color="#000000",  # Pure black
    )
    time_label.place(x=20, y=8)
    update_time()

    calibration_label = ctk.CTkLabel(
        calibration_window,
        text="LEVEL: DEV MODE",
        font=("Noto Sans Bold", 28),
        text_color="#00FF00",  # Bright green
    )
    calibration_label.place(relx=0.5, rely=0.5, anchor="center")

    return calibration_window

import customtkinter as ctk
import time


def create_debug_window(parent_app, signal_values, watched_ids):
    """Create and return the debug window"""
    debug_window = ctk.CTkToplevel(parent_app)
    debug_window.geometry("800x480")
    debug_window.title("CAN Monitor - DEV")
    debug_window.configure(cursor="arrow")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # ==== Top Bar ====
    top_bar = ctk.CTkFrame(debug_window, height=60)
    top_bar.pack(side="top", fill="x")

    line = ctk.CTkFrame(debug_window, height=3, fg_color="#FF4500")  # Bright orange
    line.pack(fill="x")

    title_label = ctk.CTkLabel(
        top_bar,
        text="CAN Monitor (DEV)",
        font=("Noto Sans Bold", 28, "bold"),
        text_color="#00FFFF",  # Bright cyan
    )
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    time_label = ctk.CTkLabel(
        top_bar,
        text="--:--",
        font=("Noto Sans Bold", 24, "bold"),
        text_color="#FF00FF",  # Bright magenta
    )
    time_label.place(x=20, rely=0.5, anchor="w")

    def update_time():
        current_time = time.strftime("%H:%M")
        time_label.configure(text=current_time)
        debug_window.after(1000, update_time)

    update_time()

    # ==== Content Area ====
    content_frame = ctk.CTkFrame(debug_window)
    content_frame.pack(fill="both", expand=True)

    content_frame.grid_columnconfigure((0, 1), weight=1)
    content_frame.grid_rowconfigure((0, 1, 2), weight=1)

    signal_labels = {}

    for idx, can_id in enumerate(watched_ids):
        row = idx // 2
        col = idx % 2

        frame_widget = ctk.CTkFrame(content_frame, corner_radius=5)
        frame_widget.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        inner_frame = ctk.CTkFrame(frame_widget)
        inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        inner_frame.grid_columnconfigure(0, weight=7)
        inner_frame.grid_columnconfigure(1, weight=3)

        signal_label = ctk.CTkLabel(
            inner_frame,
            text="Mock data...",
            justify="left",
            anchor="nw",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00FF00",  # Bright green
        )
        signal_label.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        id_label = ctk.CTkLabel(
            inner_frame,
            text=f"0x{can_id:X}",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="center",
            text_color="#FFFF00",  # Bright yellow
        )
        id_label.grid(row=0, column=1, sticky="nsew")

        signal_labels[can_id] = signal_label

    def update_signal_display():
        # Show current signal values in debug window
        for can_id in watched_ids:
            label = signal_labels[can_id]

            # Generate mock display for each CAN ID
            if can_id == 0x69:  # LV Voltage
                if "LV_Voltage" in signal_values:
                    label.configure(
                        text=f"LV_Voltage: {signal_values['LV_Voltage']:.2f}V"
                    )
                else:
                    label.configure(text="No LV_Voltage data")
            else:
                # Show some relevant signals for other IDs
                relevant_signals = []
                for signal_name, value in signal_values.items():
                    if len(relevant_signals) < 3:  # Limit to 3 signals per frame
                        relevant_signals.append(f"{signal_name}: {value}")

                if relevant_signals:
                    label.configure(text="\n".join(relevant_signals))
                else:
                    label.configure(text="Mock CAN data")

        debug_window.after(100, update_signal_display)

    update_signal_display()

    return debug_window

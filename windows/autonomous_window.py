import customtkinter as ctk


def create_autonomous_window(parent_app, signal_values):
    """Create and return the autonomous window"""
    autonomous_window = ctk.CTkToplevel(parent_app)
    autonomous_window.geometry("800x480")
    autonomous_window.configure(cursor="arrow")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # ==== Top Bar ====
    line = ctk.CTkFrame(
        autonomous_window, height=3, fg_color="#FF4500"
    )  # Bright orange
    line.pack(fill="x")

    # ==== Content Area ====
    content_frame = ctk.CTkFrame(autonomous_window)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Grid layout: 2 columns, 3 rows
    content_frame.grid_columnconfigure((0, 1), weight=1)
    content_frame.grid_rowconfigure((0, 1, 2), weight=1)

    # === Module Status Section ===
    modules_frame = ctk.CTkFrame(content_frame, corner_radius=10)
    modules_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Module status containers
    modules_container = ctk.CTkFrame(modules_frame)
    modules_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    modules_container.grid_columnconfigure((0, 1), weight=1)
    modules_container.grid_rowconfigure((0, 1), weight=1)

    # Jerson Module
    jerson_frame = ctk.CTkFrame(modules_container, corner_radius=8)
    jerson_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    jerson_title = ctk.CTkLabel(
        jerson_frame,
        text="JERSON",
        font=("Noto Sans Bold", 20, "bold"),
        text_color="#FFFFFF",
    )
    jerson_title.pack(pady=(10, 5))
    jerson_status = ctk.CTkLabel(
        jerson_frame, text="UNKNOWN", font=("Noto Sans Bold", 18, "bold")
    )
    jerson_status.pack(pady=(0, 10))

    # ACU Module
    acu_frame = ctk.CTkFrame(modules_container, corner_radius=8)
    acu_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    acu_title = ctk.CTkLabel(
        acu_frame, text="ACU", font=("Noto Sans Bold", 20, "bold"), text_color="#FFFFFF"
    )
    acu_title.pack(pady=(10, 5))
    acu_status = ctk.CTkLabel(
        acu_frame, text="UNKNOWN", font=("Noto Sans Bold", 18, "bold")
    )
    acu_status.pack(pady=(0, 10))

    # VCU Module
    vcu_frame = ctk.CTkFrame(modules_container, corner_radius=8)
    vcu_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    vcu_title = ctk.CTkLabel(
        vcu_frame, text="VCU", font=("Noto Sans Bold", 20, "bold"), text_color="#FFFFFF"
    )
    vcu_title.pack(pady=(10, 5))
    vcu_status = ctk.CTkLabel(
        vcu_frame, text="UNKNOWN", font=("Noto Sans Bold", 18, "bold")
    )
    vcu_status.pack(pady=(0, 10))

    # Maxon Module
    maxon_frame = ctk.CTkFrame(modules_container, corner_radius=8)
    maxon_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    maxon_title = ctk.CTkLabel(
        maxon_frame,
        text="MAXON",
        font=("Noto Sans Bold", 20, "bold"),
        text_color="#FFFFFF",
    )
    maxon_title.pack(pady=(10, 5))
    maxon_status = ctk.CTkLabel(
        maxon_frame, text="UNKNOWN", font=("Noto Sans Bold", 18, "bold")
    )
    maxon_status.pack(pady=(0, 10))

    # === Hydraulic Pressure Section ===
    hydraulic_frame = ctk.CTkFrame(content_frame, corner_radius=10)
    hydraulic_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    hydraulic_title = ctk.CTkLabel(
        hydraulic_frame,
        text="HYDRAULIC PRESSURE",
        font=("Noto Sans Bold", 20, "bold"),
        text_color="#FFFFFF",  # White text
    )
    hydraulic_title.pack(pady=(10, 5))

    # Front Hydraulic
    hydr_front_frame = ctk.CTkFrame(hydraulic_frame, corner_radius=5)
    hydr_front_frame.pack(fill="x", padx=10, pady=5)
    hydr_front_label = ctk.CTkLabel(
        hydr_front_frame,
        text="FRONT",
        font=("Noto Sans Bold", 18, "bold"),
        text_color="#FFFFFF",  # White text
    )
    hydr_front_label.pack(pady=5)
    hydr_front_value = ctk.CTkLabel(
        hydr_front_frame,
        text="--- bar",
        font=("Noto Sans Bold", 28, "bold"),
        text_color="#FFFFFF",  # Pure white
    )
    hydr_front_value.pack(pady=(0, 5))

    # Hydraulic Front Progress Bar
    hydr_front_bar = ctk.CTkProgressBar(
        hydr_front_frame,
        width=200,
        height=15,
        progress_color="#00FFFF",  # Bright cyan
    )
    hydr_front_bar.pack(pady=(0, 10))
    hydr_front_bar.set(0)  # Initialize to 0

    # Rear Hydraulic
    hydr_rear_frame = ctk.CTkFrame(hydraulic_frame, corner_radius=5)
    hydr_rear_frame.pack(fill="x", padx=10, pady=5)
    hydr_rear_label = ctk.CTkLabel(
        hydr_rear_frame,
        text="REAR",
        font=("Noto Sans Bold", 18, "bold"),
        text_color="#FFFFFF",  # White text
    )
    hydr_rear_label.pack(pady=5)
    hydr_rear_value = ctk.CTkLabel(
        hydr_rear_frame,
        text="--- bar",
        font=("Noto Sans Bold", 28, "bold"),
        text_color="#FFFFFF",  # Pure white
    )
    hydr_rear_value.pack(pady=(0, 5))

    # Hydraulic Rear Progress Bar
    hydr_rear_bar = ctk.CTkProgressBar(
        hydr_rear_frame,
        width=200,
        height=15,
        progress_color="#00FFFF",  # Bright cyan
    )
    hydr_rear_bar.pack(pady=(0, 10))
    hydr_rear_bar.set(0)  # Initialize to 0

    # === Pneumatic Pressure Section ===
    pneumatic_frame = ctk.CTkFrame(content_frame, corner_radius=10)
    pneumatic_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    pneumatic_title = ctk.CTkLabel(
        pneumatic_frame,
        text="PNEUMATIC PRESSURE",
        font=("Noto Sans Bold", 20, "bold"),
        text_color="#FFFFFF",  # White text
    )
    pneumatic_title.pack(pady=(10, 5))

    # Front Pneumatic
    pneu_front_frame = ctk.CTkFrame(pneumatic_frame, corner_radius=5)
    pneu_front_frame.pack(fill="x", padx=10, pady=5)
    pneu_front_label = ctk.CTkLabel(
        pneu_front_frame,
        text="FRONT",
        font=("Noto Sans Bold", 18, "bold"),
        text_color="#FFFFFF",  # White text
    )
    pneu_front_label.pack(pady=5)
    pneu_front_value = ctk.CTkLabel(
        pneu_front_frame,
        text="--- bar",
        font=("Noto Sans Bold", 28, "bold"),
        text_color="#FFFFFF",  # Pure white
    )
    pneu_front_value.pack(pady=(0, 5))

    # Pneumatic Front Progress Bar
    pneu_front_bar = ctk.CTkProgressBar(
        pneu_front_frame,
        width=200,
        height=15,
        progress_color="#00FF00",  # Bright green
    )
    pneu_front_bar.pack(pady=(0, 10))
    pneu_front_bar.set(0)  # Initialize to 0

    # Rear Pneumatic
    pneu_rear_frame = ctk.CTkFrame(pneumatic_frame, corner_radius=5)
    pneu_rear_frame.pack(fill="x", padx=10, pady=5)
    pneu_rear_label = ctk.CTkLabel(
        pneu_rear_frame,
        text="REAR",
        font=("Noto Sans Bold", 18, "bold"),
        text_color="#FFFFFF",  # White text
    )
    pneu_rear_label.pack(pady=5)
    pneu_rear_value = ctk.CTkLabel(
        pneu_rear_frame,
        text="--- bar",
        font=("Noto Sans Bold", 28, "bold"),
        text_color="#FFFFFF",  # Pure white
    )
    pneu_rear_value.pack(pady=(0, 5))

    # Pneumatic Rear Progress Bar
    pneu_rear_bar = ctk.CTkProgressBar(
        pneu_rear_frame,
        width=200,
        height=15,
        progress_color="#00FF00",  # Bright green
    )
    pneu_rear_bar.pack(pady=(0, 10))
    pneu_rear_bar.set(0)  # Initialize to 0

    def update_autonomous_data():
        # Update module statuses
        def get_status_color_text(state):
            if state == 0:
                return "ERROR", "#FF0000"  # Bright red
            elif state == 1:
                return "OK", "#00FF00"  # Bright green
            elif state == 2:
                return "WARNING", "#FFFF00"  # Bright yellow
            else:
                return "UNKNOWN", "#FF00FF"  # Bright magenta

        if "Jerson_State" in signal_values:
            status_text, color = get_status_color_text(signal_values["Jerson_State"])
            jerson_status.configure(text=status_text, text_color=color)

        if "ACU_State" in signal_values:
            status_text, color = get_status_color_text(signal_values["ACU_State"])
            acu_status.configure(text=status_text, text_color=color)

        if "VCU_State" in signal_values:
            status_text, color = get_status_color_text(signal_values["VCU_State"])
            vcu_status.configure(text=status_text, text_color=color)

        if "Maxon_State" in signal_values:
            status_text, color = get_status_color_text(signal_values["Maxon_State"])
            maxon_status.configure(text=status_text, text_color=color)

        # Update hydraulic pressures
        if "Hydraulic_Front" in signal_values:
            pressure = signal_values["Hydraulic_Front"]
            color = (
                "#00FF00"  # Bright green
                if 140 <= pressure <= 170
                else "#FFFF00"  # Bright yellow
                if 130 <= pressure <= 180
                else "#FF0000"  # Bright red
            )
            hydr_front_value.configure(text=f"{pressure:.1f} bar", text_color=color)
            # Update progress bar (0-150 bar range)
            hydr_front_bar.set(max(0, min(pressure / 150.0, 1.0)))

        if "Hydraulic_Rear" in signal_values:
            pressure = signal_values["Hydraulic_Rear"]
            color = (
                "#00FF00"  # Bright green
                if 140 <= pressure <= 170
                else "#FFFF00"  # Bright yellow
                if 130 <= pressure <= 180
                else "#FF0000"  # Bright red
            )
            hydr_rear_value.configure(text=f"{pressure:.1f} bar", text_color=color)
            # Update progress bar (0-150 bar range)
            hydr_rear_bar.set(max(0, min(pressure / 150.0, 1.0)))

        # Update pneumatic pressures
        if "Pneumatic_Front" in signal_values:
            pressure = signal_values["Pneumatic_Front"]
            color = (
                "#00FF00"  # Bright green
                if 8.0 <= pressure <= 9.5
                else "#FFFF00"  # Bright yellow
                if 7.5 <= pressure <= 10.0
                else "#FF0000"  # Bright red
            )
            pneu_front_value.configure(text=f"{pressure:.1f} bar", text_color=color)
            # Update progress bar (0-10 bar range)
            pneu_front_bar.set(max(0, min(pressure / 10.0, 1.0)))

        if "Pneumatic_Rear" in signal_values:
            pressure = signal_values["Pneumatic_Rear"]
            color = (
                "#00FF00"  # Bright green
                if 8.0 <= pressure <= 9.5
                else "#FFFF00"  # Bright yellow
                if 7.5 <= pressure <= 10.0
                else "#FF0000"  # Bright red
            )
            pneu_rear_value.configure(text=f"{pressure:.1f} bar", text_color=color)
            # Update progress bar (0-10 bar range)
            pneu_rear_bar.set(max(0, min(pressure / 10.0, 1.0)))

        autonomous_window.after(100, update_autonomous_data)

    update_autonomous_data()

    return autonomous_window

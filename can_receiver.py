import cantools
import can
import threading
import os

# Load DBC
script_dir = os.path.dirname(os.path.abspath(__file__))
dbc_path = os.path.join(script_dir, "DataDBC.dbc")
db = cantools.database.load_file(dbc_path)

# CAN interface setup
can_interface = "can0"
bus = can.interface.Bus(can_interface, interface="socketcan")

# Shared global data
signal_values = {}  # signal_name -> value
message_signals = {}  # frame_id -> {name, signals}
watched_ids = [
    0x20,
    0x21,
    0x22,
    0x23,
    0x24,
    0x60,
    0x69,
]  # Added 0x69 (105) for PDM LV_Voltage
can_activity = False  # Flag to indicate successful CAN reception


class CANSignalReceiver:
    def __init__(self):
        print("CANSignalReceiver started")
        self.start_can_thread()

    def start_can_thread(self):
        threading.Thread(target=self.read_can_messages, daemon=True).start()

    def read_can_messages(self):
        while True:
            msg = bus.recv()
            self.handle_can_message(msg)

    def handle_can_message(self, msg):
        global can_activity
        try:
            # Hardcoded handling for 0x69 (PDM)
            if msg.arbitration_id == 0x69:
                if len(msg.data) >= 2:
                    # Extract 2 bytes in big-endian format
                    lv_voltage_raw = (msg.data[0] << 8) | msg.data[1]

                    # Store the raw value in signal_values
                    signal_values["LV_Voltage"] = lv_voltage_raw

                    # Create message_signals entry for consistency
                    message_signals[0x69] = {
                        "name": "PDM_Data",
                        "signals": {"LV_Voltage": lv_voltage_raw},
                    }

                    can_activity = True
                    print(
                        f"Received PDM_Data (0x69): LV_Voltage = {lv_voltage_raw} (raw)"
                    )
                    return

            # Normal DBC decoding for other messages
            decoded_msg = db.get_message_by_frame_id(msg.arbitration_id)
            decoded_signals = decoded_msg.decode(msg.data)

            for signal, value in decoded_signals.items():
                signal_values[signal] = value

            message_signals[msg.arbitration_id] = {
                "name": decoded_msg.name,
                "signals": decoded_signals,
            }

            can_activity = True  # Set activity flag on successful decode
            print(
                f"Received {decoded_msg.name} (0x{msg.arbitration_id:X}): {decoded_signals}"
            )
        except Exception as e:
            print(f"Decode error for ID {hex(msg.arbitration_id)}: {e}")


def send_message(message_name, signal_data):
    try:
        msg = db.get_message_by_name(message_name)
        data = msg.encode(signal_data)

        can_msg = can.Message(
            arbitration_id=msg.frame_id, data=data, is_extended_id=msg.is_extended_frame
        )

        bus.send(can_msg)
        print(f"Sent {message_name} (0x{msg.frame_id:X}) with: {signal_data}")

    except Exception as e:
        print(f"Error sending {message_name}: {e}")

# rotary.py
import threading
from periphery import GPIO
from time import sleep

class RotarySwitch(threading.Thread):
    def __init__(self, gpiochip="/dev/gpiochip0", gpio_lines=None, delay=0.05):
        super().__init__()
        self.daemon = True
        self.gpiochip = gpiochip
        self.gpio_lines = gpio_lines or [20, 21, 17, 9, 10, 8]
        self.delay = delay
        self.running = False
        self.active_index = None  # Store last detected index

        self.gpios = [GPIO(gpiochip, line, "in") for line in self.gpio_lines]

    def read_states(self):
        return [gpio.read() for gpio in self.gpios]

    def run(self):
        self.running = True
        while self.running:
            states = self.read_states()

            if not all(states) and states.count(True) == 1:
                self.active_index = states.index(True)
            else:
                self.active_index = None

            sleep(self.delay)

    def get_index(self):
        """Return the currently active index or None."""
        return self.active_index

    def stop(self):
        self.running = False
        self.join()
        for gpio in self.gpios:
            gpio.close()

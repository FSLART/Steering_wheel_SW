# Windows package for Dashboard application
# This package contains all the window modules for the steering wheel dashboard

from .debug_window import create_debug_window
from .calibration_window import create_calibration_window
from .autonomous_window import create_autonomous_window
from .main_dashboard import create_main_dashboard

__all__ = [
    "create_debug_window",
    "create_calibration_window",
    "create_autonomous_window",
    "create_main_dashboard",
]

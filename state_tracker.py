import time

error_flags = {
    "MAP_DECODE_APPS_ERROR": False,
    "MAP_DECODE_VCU_ACU_STATE": False,
    "MAP_DECODE_INVERTER_ERROR": False,
    "MAP_DECODE_VCU_STATE": False,
    "MAP_DECODE_Ready2Drive_STATE": False
}

heartbeat_timestamps = {
    "MAP_DECODE_APPS_ERROR": time.time(),
    "MAP_DECODE_VCU_ACU_STATE": time.time(),
    "MAP_DECODE_INVERTER_ERROR": time.time(),
    "MAP_DECODE_VCU_STATE": time.time(),
    "MAP_DECODE_Ready2Drive_STATE": time.time()
}

module_last_state = {
    "MAP_DECODE_APPS_ERROR": 1,
    "MAP_DECODE_VCU_ACU_STATE": 1,
    "MAP_DECODE_INVERTER_ERROR": 1,
    "MAP_DECODE_VCU_STATE": 1
}

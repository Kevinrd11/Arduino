from app import get_latest_reading, get_readings_history, get_status


def test_status_reports_simulation_mode():
    payload = get_status()

    assert payload['mode'] == 'simulation'
    assert payload['arduino_connected'] is False


def test_latest_reading_returns_expected_sensor_keys():
    payload = get_latest_reading()

    assert {
        'temperature_c',
        'humidity_percent',
        'light_lux',
        'gas_ppm',
        'distance_cm',
        'motion_detected',
        'timestamp',
    } <= payload.keys()


def test_readings_history_returns_list():
    get_latest_reading()
    payload = get_readings_history()

    assert isinstance(payload, list)
    assert len(payload) >= 1

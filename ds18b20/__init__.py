import time

from flask import current_app


# open the file representing the sensor
def read_temp_raw():
    f = open(current_app.config["TEMP_SENSOR_FILE_LOCATION"], 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp_in_f():
    try:
        lines = read_temp_raw()
        # E.g.: ['4a 01 4b 46 7f ff 0c 10 10 : crc=10 YES\n', '4a 01 4b 46 7f ff 0c 10 10 t=20625\n']
        # If the DS sensor reads YES at the end of the first line, a temperature reading will exist on the second line
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return str(temp_f)
    except Exception as e:
        current_app.logger.error("Error getting temp", e)
        return str(0.0)

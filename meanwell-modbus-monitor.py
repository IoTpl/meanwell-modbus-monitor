import socket
import struct
import time
import threading
import curses

# Connection parameters
IP_ADDRESS = '192.168.88.111'
PORT = 502

# Modbus device configuration
DEVICE_ADDRESS = 0x83

# Modbus function codes
READ_HOLDING_REGISTERS = 0x03
PRESET_SINGLE_REGISTER = 0x06
READ_INPUT_REGISTERS = 0x04

# Default user decision
default_decision = 'yes'  # Change this variable to 'yes' or 'no' as needed

# Function for calculating CRC16
def crc16(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

# Function to build a request
def build_request(device_address, function_code, register_address, value=None):
    if value is None:
        request = struct.pack('>B B H H', device_address, function_code, register_address, 0x0001)
    else:
        request = struct.pack('>B B H H', device_address, function_code, register_address, value)
    request += crc16(request)
    return request

# Function for reading voltage
def get_value(s, request, multiplier=1.0):
    s.sendall(request)
    response = s.recv(1024)
    if len(response) > 4:
        register_value_bytes = response[3:5]
        register_value = int.from_bytes(register_value_bytes, byteorder='big')
        value = register_value / multiplier
        return value
    else:
        raise Exception("Response too short.")

# Function to perform Modbus queries
def perform_modbus_query(s, register_address, multiplier, description, function_code=READ_INPUT_REGISTERS):
    request = build_request(DEVICE_ADDRESS, function_code, register_address)
    value = get_value(s, request, multiplier)
    if value is not None:
        return f"{description}: {value:.2f}"
    else:
        return f"Failed to read {description}"

# Function to read power supply state
def read_power_state(s, device_address):
    request = build_request(device_address, READ_HOLDING_REGISTERS, 0x0000)
    try:
        state = get_value(s, request)
        return state
    except Exception as e:
        return f"Failed to read power state: {e}"

# Function to set power state
def set_power_state(s, device_address, turn_on):
    value = 0x0001 if turn_on else 0x0000
    request = build_request(device_address, PRESET_SINGLE_REGISTER, 0x0000, value)
    try:
        s.sendall(request)
        response = s.recv(1024)
        # Ideally, verify the response here
        return "Power state changed successfully."
    except Exception as e:
        return f"Failed to set power state: {e}"

# Function to continuously update Modbus data
def update_modbus_data(stdscr, s):
    while True:
        stdscr.clear()

        # Modbus queries
        stdscr.addstr(0, 0, perform_modbus_query(s, 0x0060, 100.0, "Output Voltage"))
        stdscr.addstr(1, 0, perform_modbus_query(s, 0x00D3, 100.0, "Battery Voltage"))
        stdscr.addstr(2, 0, perform_modbus_query(s, 0x0050, 10.0, "Input Voltage"))
        stdscr.addstr(3, 0, perform_modbus_query(s, 0x0062, 10.0, "Internal Power Supply Temperature"))
        stdscr.addstr(4, 0, perform_modbus_query(s, 0x0061, 100.0, "Output Current"))
        stdscr.addstr(5, 0, perform_modbus_query(s, 0x00D4, 1000.0, "Battery Charge/Discharge Current"))

        # Read current power supply state
        current_state = read_power_state(s, DEVICE_ADDRESS)
        if current_state is not None:
            power_state_str = "Power Supply: ON" if current_state else "Power Supply: OFF"
            stdscr.addstr(7, 0, power_state_str)

        stdscr.addstr(8, 0, "Press 'Enter' to toggle power supply")
        stdscr.addstr(9, 0, "Press 'q' to quit")

        stdscr.refresh()

        # Wait for 1 second before the next iteration
        time.sleep(1)

# Main function
def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        try:
            s.connect((IP_ADDRESS, PORT))

            # Start a separate thread to continuously update Modbus data
            modbus_thread = threading.Thread(target=update_modbus_data, args=(stdscr, s))
            modbus_thread.daemon = True
            modbus_thread.start()

            while True:
                key = stdscr.getch()

                if key == ord('q'):
                    break  # Exits the loop and ends the function
                elif key == 10:  # Enter key
                    # Read current power supply state
                    current_state = read_power_state(s, DEVICE_ADDRESS)
                    if current_state is not None:
                        result = set_power_state(s, DEVICE_ADDRESS, not current_state)
                        stdscr.addstr(10, 0, result)
                        stdscr.refresh()
                else:
                    stdscr.addstr(10, 0, "Press 'Enter' to toggle power supply")
                    stdscr.refresh()

        except socket.timeout:
            stdscr.addstr(10, 0, "Timeout while waiting for a response from the device.")
        except Exception as e:
            stdscr.addstr(10, 0, f"An error occurred: {e}")

if __name__ == "__main__":
    curses.wrapper(main)
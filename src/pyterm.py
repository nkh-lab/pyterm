#!/usr/bin/python3

#
# Copyright (C) 2024 https://github.com/nkh-lab
#
# This is free software. You can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY.
#

import serial
import threading
import sys
import select
import time

# Default read timeout value in seconds
DEFAULT_READ_TIMEOUT = 0.5

# Set up logging
DEBUG = False


def read_from_port(serial_port, stop_event, hex_mode):
    """Thread function to read data from the serial port."""
    while not stop_event.is_set():
        try:
            # Check if there is data waiting in the serial buffer
            if serial_port.in_waiting > 0:
                # Read data from the serial port
                data = serial_port.read(serial_port.in_waiting)
                if hex_mode:
                    # Decode data from bytes to hex string
                    text = data.hex()
                    print(text, end="\n", flush=True)
                else:
                    # Decode data from bytes to text
                    text = data.decode("utf-8")
                    print(text, end="", flush=True)
            else:
                # Sleep for a short time to reduce CPU usage
                time.sleep(0.1)
        except serial.SerialException as e:
            # Handle exceptions related to the serial port
            print(f"Error reading from {serial_port.port}: {e}")
            stop_event.set()
    if DEBUG:
        print("Read thread exiting...")


def main():
    if len(sys.argv) < 3:
        # Ensure the correct number of arguments are provided
        print(f"Usage: {sys.argv[0]} <port> <baudrate> [-h]")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2])
    hex_mode = "-h" in sys.argv

    try:
        # Open the serial port with the specified parameters
        serial_port = serial.Serial(
            port, baudrate, timeout=DEFAULT_READ_TIMEOUT)
        print(
            f"Connected to {port} at {baudrate} baudrate. Use Ctrl+C to exit.")
    except Exception as e:
        # Handle exceptions related to opening the serial port
        print(f"Failed to connect to {port}: {e}")
        sys.exit(1)

    # Event to signal the read thread to stop
    stop_event = threading.Event()

    # Start the reading thread
    read_thread = threading.Thread(
        target=read_from_port, args=(serial_port, stop_event, hex_mode))
    read_thread.daemon = True
    read_thread.start()

    try:
        while True:
            # Use select to wait for user input or timeout
            if select.select([sys.stdin], [], [], 0.1)[0]:
                # Pause reading thread
                stop_event.set()
                read_thread.join()

                # Read user input from the console, '\n' - stripped
                user_input = input()
                if user_input:
                    if hex_mode:
                        # Convert hex string to binary data
                        try:
                            # Split hex string into pairs of hex digits
                            bytes_to_send = bytes.fromhex(user_input)
                        except ValueError as e:
                            print(f"Invalid hex input: {e}")
                    else:
                        # Text mode
                        bytes_to_send = (user_input + "\n").encode("utf-8")

                    # Send the user input to the serial port
                    serial_port.write(bytes_to_send)

                # Restart the reading thread
                stop_event.clear()
                read_thread = threading.Thread(
                    target=read_from_port, args=(serial_port, stop_event, hex_mode))
                read_thread.daemon = True
                read_thread.start()
    except KeyboardInterrupt:
        # Handle the user pressing Ctrl+C to exit
        print("\nExiting...")
    finally:
        # Signal the reading thread to stop
        stop_event.set()
        # Wait for the reading thread to finish
        read_thread.join()
        # Close the serial port
        serial_port.close()
        print("Serial port closed.")


if __name__ == "__main__":
    main()

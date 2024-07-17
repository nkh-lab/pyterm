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

import pytest
import pexpect
import time
import os
import signal

PYTERM = "./../src/pyterm.py"


@pytest.fixture(scope="module")
def virtual_serial_ports():
    """
    Create a pair of connected virtual serial ports for testing.
    """
    # Start the socat process to create a pair of PTY devices
    command = 'socat -d -d pty,raw,echo=0 pty,raw,echo=0'
    process = pexpect.spawn(command, timeout=10)

    # Wait for the PTY messages to confirm that socat is running
    try:
        process.expect(r'PTY is (\S+)')
        pty1 = process.match.group(1).decode('utf-8')
        process.expect(r'PTY is (\S+)')
        pty2 = process.match.group(1).decode('utf-8')
    except pexpect.TIMEOUT as e:
        process.kill(0)  # Kill the process if we timeout
        raise Exception(f"Timeout waiting for PTY names: {e}")
    except pexpect.EOF as e:
        process.kill(0)  # Kill the process on unexpected EOF
        raise Exception(f"Unexpected EOF while waiting for PTY names: {e}")

    # Yield the PTY paths for the test cases
    yield pty1, pty2

    # Terminate the socat process after tests
    process.terminate()
    process.wait()


def test_handshake(virtual_serial_ports):
    port1, port2 = virtual_serial_ports

    # Spawn the first instance of the terminal script
    terminal1 = pexpect.spawn(f"{PYTERM} {port1} 9600")
    terminal1.expect(f"Connected to {port1} at 9600 baudrate")

    # Spawn the second instance of the terminal script
    terminal2 = pexpect.spawn(f"{PYTERM} {port2} 9600")
    terminal2.expect(f"Connected to {port2} at 9600 baudrate")

    time.sleep(1)  # Give some time for the terminals to set up

    # Send handshake message from terminal1
    terminal1.sendline("Hello from Terminal1!")
    terminal1.expect("Hello from Terminal1!")

    # Check if terminal2 received the handshake message
    terminal2.expect("Hello from Terminal1!")

    # Send handshake response from terminal2
    terminal2.sendline("Hello from Terminal2!")
    terminal2.expect("Hello from Terminal2!")

    # Check if terminal1 received the handshake response
    terminal1.expect("Hello from Terminal2!")

    # Close terminals
    terminal1.close()
    terminal2.close()


def test_handshake_hex(virtual_serial_ports):
    port1, port2 = virtual_serial_ports

    # Spawn the first instance of the terminal script in hex mode
    terminal1 = pexpect.spawn(f"{PYTERM} {port1} 9600 -h")
    terminal1.expect(f"Connected to {port1} at 9600 baudrate")

    # Spawn the second instance of the terminal script in hex mode
    terminal2 = pexpect.spawn(f"{PYTERM} {port2} 9600 -h")
    terminal2.expect(f"Connected to {port2} at 9600 baudrate")

    time.sleep(1)  # Give some time for the terminals to set up

    # Send handshake message from terminal1 (Hex for "Hello")
    terminal1.sendline("48656c6c6f")  # Hex for "Hello"
    # Expect the same hex string (loopback check)
    terminal1.expect("48656c6c6f")

    # Check if terminal2 received the handshake message (Hex for "Hello")
    terminal2.expect("48656c6c6f")  # Expect the same hex string (received)

    # Send handshake response from terminal2 (Hex for "Hello from Terminal2")
    terminal2.sendline("48656c6c6f2066726f6d204d616e7954")
    # Expect the same hex string (loopback check)
    terminal2.expect("48656c6c6f2066726f6d204d616e7954")

    # Check if terminal1 received the handshake response (Hex for "Hello from Terminal2")
    # Expect the same hex string (received)
    terminal1.expect("48656c6c6f2066726f6d204d616e7954")

    # Close terminals
    terminal1.close()
    terminal2.close()

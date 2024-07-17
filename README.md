## Intro
This project is a Python-based serial port terminal designed with a simple and user-friendly interface. It's easy to use for various DIY projects, such as communicating with an Arduino or other microcontroller via the serial port.

## How It Works
After running the terminal, it starts listening to the specified serial port for incoming data. When the user begins typing, the terminal temporarily pauses listening. Upon pressing Enter, the typed data is sent to the connected device, and the terminal resumes listening to the port for any new messages. This allows for seamless communication between the terminal and the connected device.

## Prerequisites
```
pip install serial
```
Or for Ubuntu:
```
sudo apt install python3-serial
```

## Usage and Input Arguments
If you run the script without any arguments passed, you will see a usage hint:
```
./pyterm.py
Usage: ./pyterm.py <port> <baudrate> [-h]
```
Passing the -h flag enables hexadecimal mode, which means you can send raw bytes, otherwise text mode will be used.

## Examples of usage
Text mode:
```
./pyterm.py /dev/pts/13 9600
Connected to /dev/pts/13 at 9600 baudrate. Use Ctrl+C to exit.
Hello World from pyterm!
```

Hex mode:
```
./pyterm.py /dev/pts/13 9600 -h
Connected to /dev/pts/13 at 9600 baudrate. Use Ctrl+C to exit.
0102030405060708090a0b0c0d0e0f
```

## Other documentation
In the [doc](./doc) folder you can find other documentation related to this project and this topic.
## How to setup virtual serial ports on Ubuntu
1. Install socat:
```
sudo apt-get install socat
```
2. Create a pair of virtual serial ports:
```
socat -d -d pty,raw,echo=0 pty,raw,echo=0
2024/07/17 09:44:29 socat[2497321] N PTY is /dev/pts/13
2024/07/17 09:44:29 socat[2497321] N PTY is /dev/pts/18
2024/07/17 09:44:29 socat[2497321] N starting data transfer loop with FDs [5,5] and [7,7]
```
3. Test the terminal script:

Termial#1:
```
./pyterm.py /dev/pts/13 9600
Connected to /dev/pts/13 at 9600 baudrate with a read timeout of 0.5 seconds. Use Ctrl+C to exit.
Hello from Terminal#1
Hello from Terminal#2
^C
Exiting...
Serial port closed.
```

Termial#2:
```
./pyterm.py /dev/pts/13 9600
Connected to /dev/pts/13 at 9600 baudrate with a read timeout of 0.5 seconds. Use Ctrl+C to exit.
Hello from Terminal#1
Hello from Terminal#2
^C
Exiting...
Serial port closed.
```

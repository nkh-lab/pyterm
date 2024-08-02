## Via symlink in Linux
1. Create a new symlink:
```
ln -s ~/Projects/my/pyterm/src/pyterm.py ~/bin/pyterm
```
2. Usage example:
```
pyterm /dev/pts/9 115200
Connected to /dev/pts/9 at 115200 baudrate. Use Ctrl+C to exit.
Hello!
```
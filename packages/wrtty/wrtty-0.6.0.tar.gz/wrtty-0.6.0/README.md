# wrtty
`wrtty` is a Python script to write commands to a virtual terminal.

Note: `wrtty` elevates permissions with `sudo`
because it needs root permissions.

By "virtual terminal", it is meant what is often called the "console",
which is slightly different.
In this case it is the "virtual terminal" controlled by commands such
as `chvt` (e.g. `sudo chvt 3`).

Writing to the console can make text appear, but it won't make it execute
as a command in a shell.
Writing to the virtual terminal, such as `/dev/tty1`, commands can be
run, login on console, etc.

This may be used in a situation where you have ssh access to a machine,
but no X/Wayland/VNC running,
but you need to run as if you are in front of the machine.
This in effect simulates an operator standing in front of a machine,
typing on the local keyboard.


# Install
Install from PyPI.

```
pip install wrtty
```


# Help
Help output:

```
$ wrtty -h
usage: wrtty [-h] [-c CMD] [-t TTY]

write command to virtual terminal

options:
  -h, --help         show this help message and exit
  -c CMD, --cmd CMD  command to run (default echo)
  -t TTY, --tty TTY  TTY to use (default /dev/tty1)
```


# Use
Use examples:

```
wrtty
wrtty -c "date -uR"
wrtty -t /dev/tty2 --cmd "clear"
```


# Build
Developers build thusly.

Under Debian stable (Bookworm/12).

Python setup, suit to taste:

```
git clone https://spacecruft.org/deepcrayon/wrtty
cd wrtty/
pyenv local 3.11 # if pyenv
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel poetry
poetry install
```


# Status
WORKSFORME.


# Upstream
I don't know of another application that specifically does this.
There are a few old snippets in perl, C, and Python in StackExchange
and blogs, but just small examples.

Some linkies:


fcntl — The fcntl and ioctl system calls
* https://docs.python.org/3/library/fcntl.html

Faking input with IOCTL/TIOCSTI
* https://kristian.ronningen.no/linux/faking-input-with-ioctl-tiocsti/

RichardBronosky writevt.c
* https://gist.github.com/RichardBronosky/62a4fc8531a169abb811

Construct a command by putting a string into a tty
* https://unix.stackexchange.com/questions/48103/construct-a-command-by-putting-a-string-into-a-tty

Unable to fake terminal input with termios.TIOCSTI
* https://stackoverflow.com/questions/29614264/unable-to-fake-terminal-input-with-termios-tiocsti/29616465

send command to another terminal
* https://riowingwp.wordpress.com/2022/01/23/command-to-terminal/

Can I send some text to the STDIN of an active process running in a screen session?
* https://serverfault.com/questions/178457/can-i-send-some-text-to-the-stdin-of-an-active-process-running-in-a-screen-sessi


# Linux Kernel Note
I see this configuration option and note in a 6.5 kernel:

```
CONFIG_LEGACY_TIOCSTI:
Historically the kernel has allowed TIOCSTI, which will push
characters into a controlling TTY. This continues to be used
as a malicious privilege escalation mechanism, and provides no
meaningful real-world utility any more. Its use is considered
a dangerous legacy operation, and can be disabled on most
systems.

Say Y here only if you have confirmed that your system's
userspace depends on this functionality to continue operating
normally.

Processes which run with CAP_SYS_ADMIN, such as BRLTTY, can
use TIOCSTI even when this is set to N.

This functionality can be changed at runtime with the
dev.tty.legacy_tiocsti sysctl. This configuration option sets
the default value of the sysctl.

Symbol: LEGACY_TIOCSTI [=y]
Type  : bool
Defined at drivers/tty/Kconfig:152
Prompt: Allow legacy TIOCSTI usage
Depends on: TTY [=y]
  Location:
    -> Device Drivers
      -> Character devices
        -> Enable TTY (TTY [=y])
          -> Allow legacy TIOCSTI usage (LEGACY_TIOCSTI [=y])
```

:)


# License
MIT.

*Copyright &copy; 2023, 2024, Jeff Moe.*


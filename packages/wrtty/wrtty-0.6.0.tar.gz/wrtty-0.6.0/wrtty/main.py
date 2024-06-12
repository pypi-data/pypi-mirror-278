# MIT License
#
# Copyright (c) 2023, 2024 Jeff Moe
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
wrtty --- write command to virtual terminal.
"""
import argparse
import fcntl
import os
import sys
import termios


def parse_args():
    parser = argparse.ArgumentParser(description="write string to tty virtual terminal")
    parser.add_argument(
        "-s",
        "--string",
        help="string to write (default echo)",
        type=str,
        required=False,
        default="echo",
    )
    parser.add_argument(
        "-t",
        "--tty",
        help="TTY to use (default /dev/tty1)",
        type=str,
        required=False,
        default="/dev/tty1",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    CMD = args.string
    TTY = args.tty

    if os.geteuid() != 0:
        os.execvpe("sudo", ["sudo", sys.argv[0]] + sys.argv[1:], os.environ)

    with open(TTY, "w") as fd:
        for char in CMD:
            print(char, end="")
            fcntl.ioctl(fd, termios.TIOCSTI, char)
        fcntl.ioctl(fd, termios.TIOCSTI, "\n")
        print()


if __name__ == "__main__":
    main()

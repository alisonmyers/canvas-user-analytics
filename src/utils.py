import sys

def print_success(msg):
    print(f"\033[0;32m{msg}\033[0m")

def print_unexpected(msg):
    print(f"\033[0;31m{msg}\033[0m")

def shut_down(msg):
    print(msg)
    print("Shutting down...")
    sys.exit()

# src/util.py
"""
Utility functions for printing and logging without causing circular imports.
"""

import sys
from colorama import init

init()

# --- Console printing helpers ---
def print_success(msg):
    """Print a success message to console."""
    print(f"\033[0;32mSUCCESS:\033[0m {msg}")

def print_unexpected(msg):
    """Print an unexpected/failure message to console."""
    print(f"\033[0;31mFAIL:\033[0m {msg}")

def shut_down(msg):
    """Print shutdown message and exit script."""
    print(msg)
    print("Shutting down...")
    sys.exit()

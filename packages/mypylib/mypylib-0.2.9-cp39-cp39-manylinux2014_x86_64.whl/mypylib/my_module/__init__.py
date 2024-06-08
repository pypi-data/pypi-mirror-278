import os
import ctypes
import sys

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), 'libcallback_example.so')
callback_example = ctypes.CDLL(lib_path)

# Define the callback type in ctypes
CALLBACK_TYPE = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

# Define the Python callback function
def my_callback(value):
    print(f"In Python: Callback called with value: {value.decode('utf-8')}")

# Convert the Python callback to a C callback
c_callback = CALLBACK_TYPE(my_callback)

# Set the argument types for the C functions
callback_example.start_thread.argtypes = [CALLBACK_TYPE]
callback_example.stop_thread.argtypes = []

# Start the thread with the callback
def start():
    callback_example.start_thread(c_callback)

# Stop the thread
def stop():
    callback_example.stop_thread()

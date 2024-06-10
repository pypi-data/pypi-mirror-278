# hello.py
import os
import ctypes

# Get the path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the shared library
lib_path = os.path.join(current_dir, 'libhello.so')
libhello = ctypes.CDLL(lib_path)

# Define the function prototype
print_hello_muneeb = libhello.print_hello_muneeb
print_hello_muneeb.restype = None

# Function to call the C function
def say_hello():
    print_hello_muneeb()
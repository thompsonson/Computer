"""This file is used to add the parent directory of the models package to the Python path when the tests are called."""
import os
import sys

# Add the parent directory of the models package to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(f"inserted {os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))}")

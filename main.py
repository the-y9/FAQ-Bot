import importlib
import sys
import os
v = 'v2'
v1_path = os.path.join(os.path.dirname(__file__), v)
sys.path.append(v1_path)

# Dynamically import the module
v_main = importlib.import_module(f'{v}.main')

if hasattr(v_main, 'main'):
    v_main.main()

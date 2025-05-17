import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(base_dir)

from base.langflow.database.init_db import init_db

if __name__ == "__main__":
    init_db() 
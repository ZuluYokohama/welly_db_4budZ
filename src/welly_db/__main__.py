"""
python -m src.welly_db

Launches the studio engine (equivalent to scripts/run_studio.py).
"""

from pathlib import Path
import sys

# Make runnable as module
if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.run_studio import main

if __name__ == "__main__":
    main()

from pathlib import Path

# -----------------------------------------------------
# Paths

# config.py lives in <project>/src/core/.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DATA_RAW_PATH = RAW_DATA_DIR / "dataset_metacritic_scraper_2025-02-15.csv"
DATA_FORMATTED_PATH = PROCESSED_DATA_DIR / "dataset_metacritic_scraper_reformatted.csv"

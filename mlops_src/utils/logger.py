# mlops_src/utils/logger.py
import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str, log_file: str) -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # 1. Write the high-level ledger entry to the file
    run_count = 1
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            run_count = sum(1 for _ in f) + 1
            
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} -> {name} run {run_count}\n")

    # 2. Detailed logs go ONLY to stdout (GitHub Actions workspace)
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    
    logger.addHandler(ch)
    
    return logger

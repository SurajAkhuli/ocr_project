import os
import time

def log_message(message: str, level: str = 'INFO'):
    """
    Logs a message to the console with a timestamp and severity level.
    This utility function helps maintain a clear audit trail of processing steps.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{timestamp}] [{level}] {message}")

def safe_file_read(filepath: str, mode: str = 'r'):
    """
    Safely reads content from a file, handling FileNotFoundError.
    (Primarily a placeholder for future testing/file-based utilities)
    """
    try:
        with open(filepath, mode) as f:
            return f.read()
    except FileNotFoundError:
        log_message(f"File not found: {filepath}", 'ERROR')
        return None
    except Exception as e:
        log_message(f"An unexpected error occurred reading {filepath}: {e}", 'ERROR')
        return None
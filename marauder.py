#!/usr/bin/env python3
"""
marauder.py - A sample Python utility module

This module demonstrates various utility functions commonly used
in automation scripts. It includes helpers for file handling,
text processing, and system information retrieval.

Author: Rahul Manna
Created: 2026-10-14
Version: 1.0.0
"""

import os
import sys
import json
import time
import random
import hashlib
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


# ============================================================
# Configuration Constants
# ============================================================

APP_NAME = "Marauder"
APP_VERSION = "1.0.0"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
SUPPORTED_PLATFORMS = ["Windows", "Linux", "Darwin"]


# ============================================================
# Utility Functions
# ============================================================

def get_system_info() -> Dict[str, Any]:
    """
    Retrieve basic system information.
    
    Returns:
        dict: A dictionary containing system details such as
              OS name, version, architecture, and Python version.
    """
    return {
        "os": platform.system(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "timestamp": datetime.now().isoformat()
    }


def generate_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Generate a hash for the given data.
    
    Args:
        data: The input string to hash.
        algorithm: Hash algorithm (default: sha256).
    
    Returns:
        str: Hexadecimal hash string.
    """
    hasher = hashlib.new(algorithm)
    hasher.update(data.encode("utf-8"))
    return hasher.hexdigest()


def format_bytes(size: int) -> str:
    """
    Convert bytes to a human-readable format.
    
    Args:
        size: Size in bytes.
    
    Returns:
        str: Formatted size like '1.5 MB'.
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    value = float(size)
    
    while value >= 1024 and index < len(units) - 1:
        value /= 1024
        index += 1
    
    return f"{value:.2f} {units[index]}"


def read_file_safely(filepath: str) -> Optional[str]:
    """
    Read a file's content safely with error handling.
    
    Args:
        filepath: Path to the file.
    
    Returns:
        str or None: File content or None if error occurs.
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8")
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}")
        return None


def write_file_safely(filepath: str, content: str) -> bool:
    """
    Write content to a file safely.
    
    Args:
        filepath: Destination file path.
        content: Content to write.
    
    Returns:
        bool: True on success, False otherwise.
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except (IOError, OSError) as e:
        print(f"Error writing file: {e}")
        return False


# ============================================================
# Text Processing Helpers
# ============================================================

class TextProcessor:
    """
    A simple text processor with various utility methods.
    """
    
    def __init__(self, text: str = ""):
        self.text = text
    
    def word_count(self) -> int:
        """Return the number of words in the text."""
        return len(self.text.split())
    
    def char_count(self) -> int:
        """Return the number of characters."""
        return len(self.text)
    
    def line_count(self) -> int:
        """Return the number of lines."""
        return len(self.text.splitlines())
    
    def to_upper(self) -> str:
        """Convert text to uppercase."""
        return self.text.upper()
    
    def to_lower(self) -> str:
        """Convert text to lowercase."""
        return self.text.lower()
    
    def reverse(self) -> str:
        """Reverse the text."""
        return self.text[::-1]
    
    def replace_words(self, old: str, new: str) -> str:
        """Replace all occurrences of a word."""
        return self.text.replace(old, new)


# ============================================================
# File Operations
# ============================================================

class FileManager:
    """
    Handles file system operations.
    """
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
    
    def list_files(self, extension: str = None) -> List[str]:
        """List all files, optionally filtered by extension."""
        if extension:
            pattern = f"*.{extension.lstrip('.')}"
            return [str(f) for f in self.base_path.rglob(pattern)]
        return [str(f) for f in self.base_path.rglob("*") if f.is_file()]
    
    def file_size(self, filepath: str) -> int:
        """Return file size in bytes."""
        return Path(filepath).stat().st_size
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file if it exists."""
        try:
            Path(filepath).unlink()
            return True
        except (FileNotFoundError, PermissionError):
            return False


# ============================================================
# Main Entry Point
# ============================================================

def main() -> int:
    """
    Main function to demonstrate the module functionality.
    
    Returns:
        int: Exit code (0 = success).
    """
    print(f"=== {APP_NAME} v{APP_VERSION} ===")
    print()
    
    # Display system information
    info = get_system_info()
    print("System Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    
    # Demonstrate text processing
    sample = "Hello world this is a sample text 42"
    processor = TextProcessor(sample)
    
    print("Text Processing Demo:")
    print(f"  Original: {sample}")
    print(f"  Words: {processor.word_count()}")
    print(f"  Characters: {processor.char_count()}")
    print(f"  Uppercase: {processor.to_upper()}")
    print()
    
    # Demonstrate hashing
    hash_value = generate_hash(sample)
    print(f"SHA256: {hash_value}")
    print()
    
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

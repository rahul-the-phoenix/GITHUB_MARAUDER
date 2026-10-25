# Marauder 🚀

> A lightweight Python utility module packed with handy helpers for file handling, text processing, hashing, and system information retrieval — perfect for automation scripts and developer tooling.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 📖 Overview

**Marauder** is a self-contained, zero-dependency Python utility module that bundles the most commonly needed helpers for automation and scripting tasks into a single, clean, and well-documented file. Whether you need to grab system details, hash a string, read files safely, or process text — Marauder has you covered.

No pip installs. No virtual environments. Just drop it in and go.

---

## ✨ Features

- 🖥️ **System Information** — Fetch OS, architecture, hostname, and Python version in one call
- 🔐 **Hashing** — Generate cryptographic hashes (SHA-256 by default, any `hashlib` algorithm supported)
- 📁 **Safe File I/O** — Read and write files with built-in error handling and auto-directory creation
- 📝 **Text Processing** — Count words/chars/lines, transform case, reverse, and replace
- 🗂️ **File Management** — List files by extension, check sizes, and delete safely
- 📏 **Human-Readable Sizes** — Convert raw bytes into `KB`, `MB`, `GB`, etc.
- 🧩 **Type-Hinted & Documented** — Full type annotations and docstrings on every function

---

## 📦 Installation

No installation required. Simply copy `marauder.py` into your project directory.

If you'd like to keep it in a repository, clone it:

```bash
git clone https://github.com/yourusername/marauder.git
cd marauder
```

---

## 🚀 Quick Start

Run the built-in demo to see Marauder in action:

```bash
python3 marauder.py
```

**Sample output:**

```
=== Marauder v1.0.0 ===

System Information:
  os: Linux
  version: #1 SMP ...
  architecture: x86_64
  python_version: 3.11.4
  hostname: dev-machine
  timestamp: 2026-10-14T10:23:45.123456

Text Processing Demo:
  Original: Hello world this is a sample text 42
  Words: 8
  Characters: 38
  Uppercase: HELLO WORLD THIS IS A SAMPLE TEXT 42

SHA256: 8f434346648f6b96df89dda961c5176b10a6d83961dd3c1ac88b59b2dc327aa4

Done.
```

---

## 🧠 Usage Examples

### System Information

```python
from marauder import get_system_info

info = get_system_info()
print(f"Running on {info['os']} ({info['architecture']})")
print(f"Hostname: {info['hostname']}")
```

### Hashing

```python
from marauder import generate_hash

# Default SHA-256
digest = generate_hash("my secret data")
print(digest)

# Choose any hashlib-supported algorithm
md5 = generate_hash("my secret data", algorithm="md5")
sha1 = generate_hash("my secret data", algorithm="sha1")
```

### Byte Formatting

```python
from marauder import format_bytes

print(format_bytes(1024))           # 1.00 KB
print(format_bytes(1048576))        # 1.00 MB
print(format_bytes(5_368_709_100))  # 5.00 GB
```

### Safe File I/O

```python
from marauder import read_file_safely, write_file_safely

# Writing — creates parent directories automatically
success = write_file_safely("output/report.txt", "Hello, Marauder!")
print(f"Write successful: {success}")

# Reading — returns None on failure instead of raising
content = read_file_safely("output/report.txt")
if content:
    print(content)
```

### Text Processing

```python
from marauder import TextProcessor

tp = TextProcessor("The quick brown fox jumps over the lazy dog")

print(tp.word_count())                 # 9
print(tp.char_count())                 # 43
print(tp.to_upper())                   # THE QUICK BROWN FOX...
print(tp.reverse())                    # god yzal eht revo...
print(tp.replace_words("fox", "cat"))  # The quick brown cat...
```

### File Management

```python
from marauder import FileManager

fm = FileManager("./logs")

# List all .log files recursively
for log in fm.list_files(extension="log"):
    print(log, fm.file_size(log), "bytes")

# Clean up
fm.delete_file("logs/old.log")
```

---

## 🗂️ Module Structure

```
marauder.py
│
├── Configuration Constants
│   ├── APP_NAME, APP_VERSION
│   ├── DEFAULT_TIMEOUT, MAX_RETRIES
│   └── SUPPORTED_PLATFORMS
│
├── Utility Functions
│   ├── get_system_info()
│   ├── generate_hash()
│   ├── format_bytes()
│   ├── read_file_safely()
│   └── write_file_safely()
│
├── TextProcessor (class)
│   ├── word_count(), char_count(), line_count()
│   ├── to_upper(), to_lower(), reverse()
│   └── replace_words()
│
├── FileManager (class)
│   ├── list_files(), file_size()
│   └── delete_file()
│
└── main() — demonstration entry point
```

---

## 📋 API Reference

| Function / Method | Description | Returns |
|---|---|---|
| `get_system_info()` | Retrieve OS, version, architecture, hostname, timestamp | `Dict[str, Any]` |
| `generate_hash(data, algorithm="sha256")` | Hash a string using any `hashlib` algorithm | `str` |
| `format_bytes(size)` | Convert bytes to human-readable string | `str` |
| `read_file_safely(filepath)` | Read file content with error handling | `Optional[str]` |
| `write_file_safely(filepath, content)` | Write content, creating parent dirs | `bool` |
| `TextProcessor.word_count()` | Count words | `int` |
| `TextProcessor.char_count()` | Count characters | `int` |
| `TextProcessor.line_count()` | Count lines | `int` |
| `TextProcessor.to_upper()` / `to_lower()` | Case transformation | `str` |
| `TextProcessor.reverse()` | Reverse text | `str` |
| `TextProcessor.replace_words(old, new)` | Word replacement | `str` |
| `FileManager.list_files(extension=None)` | Recursively list files | `List[str]` |
| `FileManager.file_size(filepath)` | Get file size in bytes | `int` |
| `FileManager.delete_file(filepath)` | Safely delete a file | `bool` |

---

## ✅ Requirements

- **Python 3.7+**
- **Zero external dependencies** — uses only the Python standard library:
  - `os`, `sys`, `json`, `time`, `random`, `hashlib`, `platform`, `subprocess`
  - `datetime`, `pathlib`, `typing`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the `LICENSE` file for details.

---

## 👤 Author

**Rahul Manna**

- Created: 2026-10-14
- Version: 1.0.0

---

## ⭐ Show Your Support

If Marauder saved you time, consider giving the repo a ⭐ — it means a lot!

---

> _"Automate the boring stuff, one utility at a time."_ 🛠️

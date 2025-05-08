# images2webp

Convert all kinds of images (JPG, PNG, BMP, HEIC, etc.) to WebP format via command-line.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📦 Features

- 🔁 Supports JPG, PNG, BMP, TIFF, GIF, and HEIC formats
- 📁 Converts a single directory or recursively scans subdirectories
- 🗑️ Option to delete original files after conversion
- 🪵 Logging with optional file output
- ❌ Robust error handling and skipping invalid files

## 🚀 Usage

### Install Dependencies

First, set up a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Linux systems with HEIC support:

```bash
sudo apt install libheif-dev libde265-dev
```

### Run Script

```bash
python images2webp.py <input_dir> <output_dir> [options]
```

### Options

| Option           | Description                          |
|------------------|--------------------------------------|
| `-r, --recursive` | Recursively scan input directories   |
| `-d, --delete`    | Delete original files after convert  |
| `-l, --logfile`   | Write logs to a specified file       |

### Example

```bash
python images2webp.py ./images ./webp --recursive --delete --logfile convert.log
```

## 📝 License

MIT License © 2025 [Max Base](https://github.com/BaseMax)

See [LICENSE](LICENSE) for details.

## 🔗 Repository

https://github.com/BaseMax/images2webp

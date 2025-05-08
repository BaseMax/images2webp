import os
import argparse
import logging
from pathlib import Path
from PIL import Image
import pyheif

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.heic'}
WEBP_EXTENSION = '.webp'

def setup_logger(logfile=None):
    logger = logging.getLogger("ImageConverter")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if logfile:
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def is_supported_image(file_path):
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS

def convert_heic_to_image(file_path):
    try:
        heif_file = pyheif.read(file_path)
        return Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    except pyheif.error.HeifError as e:
        raise RuntimeError(f"[ERROR] ❌ Failed to read HEIC image: {file_path} - {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read HEIC image: {e}")

def convert_image(input_path: Path, output_path: Path, logger):
    try:
        if input_path.suffix.lower() == ".heic":
            image = convert_heic_to_image(input_path)
        else:
            image = Image.open(input_path)

        image.convert("RGB").save(output_path, "WEBP")
        logger.info(f"✅ Converted: {input_path} -> {output_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Conversion failed: {input_path} - {e}")
        return False

def convert_all_images(input_dir: Path, output_dir: Path, delete=False, recursive=False, logger=None):
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    search_paths = input_dir.rglob('*') if recursive else input_dir.glob('*')

    for file in search_paths:
        if not file.is_file() or not is_supported_image(file):
            continue

        relative_path = file.relative_to(input_dir)
        output_file_path = output_dir.joinpath(relative_path).with_suffix(WEBP_EXTENSION)
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        if output_file_path.exists():
            logger.info(f"⏭️ Skipping (already exists): {output_file_path}")
            continue

        success = convert_image(file, output_file_path, logger)
        if success and delete:
            try:
                file.unlink()
                logger.info(f"🗑️ Deleted original: {file}")
            except Exception as e:
                logger.warning(f"⚠️ Could not delete {file}: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert images to WebP format with logging and error handling."
    )
    parser.add_argument("input", help="Input directory containing images")
    parser.add_argument("output", help="Output directory for WebP images")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan directories recursively")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete original files after conversion")
    parser.add_argument("-l", "--logfile", help="Path to log file (optional)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    logger = setup_logger(args.logfile)

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    logger.info(f"🔍 Input: {input_path}")
    logger.info(f"📤 Output: {output_path}")
    logger.info(f"🌀 Recursive: {'Yes' if args.recursive else 'No'}")
    logger.info(f"🗑️ Delete Originals: {'Yes' if args.delete else 'No'}")

    convert_all_images(input_path, output_path, delete=args.delete, recursive=args.recursive, logger=logger)

if __name__ == "__main__":
    main()

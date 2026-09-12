from pathlib import Path

from PIL import Image

from src.config import (
    GOLD_DIR,
    PROTOTYPE_DIR,
    IMAGE_EXTENSIONS
)


def get_image_paths(directory: Path):
    """
    Get all supported image files from a directory.
    """

    if not directory.exists():
        return []

    image_paths = []

    for path in directory.rglob("*"):

        if (
            path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
        ):
            image_paths.append(path)

    return sorted(image_paths)


def get_gold_image_paths():
    """
    Get all gold product images.
    """

    return get_image_paths(GOLD_DIR)


def get_prototype_image_paths():
    """
    Get all prototype images.
    """

    return get_image_paths(PROTOTYPE_DIR)


def load_image(image_path):
    """
    Load an image and convert it to RGB, handling transparency by compositing over a white background.
    """
    image = Image.open(image_path)

    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        rgba_image = image.convert("RGBA")
        background = Image.new("RGB", rgba_image.size, (255, 255, 255))
        background.paste(rgba_image, mask=rgba_image.split()[3])
        return background

    return image.convert("RGB")
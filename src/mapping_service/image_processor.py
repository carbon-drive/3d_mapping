"""
Image processor for handling image uploads and preprocessing.
"""

import os
from typing import List, Dict, Any, Optional
from PIL import Image
import numpy as np


class ImageProcessor:
    """Handles image loading, validation, and preprocessing."""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self, upload_dir: str = "uploads"):
        """
        Initialize the ImageProcessor.

        Args:
            upload_dir: Directory to save uploaded images
        """
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def validate_image(self, file_path: str) -> bool:
        """
        Validate if a file is a supported image format.

        Args:
            file_path: Path to the image file

        Returns:
            True if valid, False otherwise
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return False

        # Check file extension
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.SUPPORTED_FORMATS:
            return False

        # Check file size
        if os.path.getsize(file_path) > self.MAX_IMAGE_SIZE:
            return False

        # Try to open with PIL
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def load_image(self, file_path: str) -> Optional[np.ndarray]:
        """
        Load an image and convert it to a numpy array.

        Args:
            file_path: Path to the image file

        Returns:
            Image as numpy array (HxWx3) or None if loading fails
        """
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")
                return np.array(img)
        except Exception as e:
            print(f"Error loading image {file_path}: {e}")
            return None

    def preprocess_images(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Preprocess a list of images for MapAnything inference.

        Args:
            file_paths: List of paths to image files

        Returns:
            List of view dictionaries ready for MapAnything
        """
        views = []
        for file_path in file_paths:
            if not self.validate_image(file_path):
                print(f"Skipping invalid image: {file_path}")
                continue

            img_array = self.load_image(file_path)
            if img_array is not None:
                views.append({
                    "img": img_array,
                    "file_path": file_path,
                })

        return views

    def save_uploaded_file(self, file_data: bytes, filename: str) -> str:
        """
        Save an uploaded file to the upload directory.

        Args:
            file_data: Binary file data
            filename: Original filename

        Returns:
            Path to the saved file
        """
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(self.upload_dir, safe_filename)

        with open(file_path, "wb") as f:
            f.write(file_data)

        return file_path
